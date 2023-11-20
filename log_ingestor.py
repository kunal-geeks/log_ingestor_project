import re
from flask import Flask, jsonify, request, render_template, redirect, session, url_for, g
from flask_restful import Resource, Api
from flask_pymongo import ASCENDING
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from database import get_db, init_app
from datetime import datetime
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates')
api = Api(app)

mongo_uri = os.getenv('MONGODB_URI')

if not mongo_uri:
    raise ValueError("MONGODB_URI environment variable is not set.")

client = MongoClient(mongo_uri, server_api=ServerApi('1'))

# Connect to MongoDB and create index using the admin user
try:
    # Create an index on the timestamp field for improved search performance
    log_collection = client.logs.logs_data
    log_collection.create_index([('timestamp', ASCENDING)])

    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
# SQLite configuration for user management
init_app(app)

class LogIngestor(Resource):
    def post(self):
        try:
            log_data = request.get_json()

            # Convert timestamp to MongoDB-compatible format
            log_data['timestamp'] = datetime.strptime(log_data['timestamp'], "%Y-%m-%dT%H:%M:%SZ")

            # Store logs in MongoDB
            log_collection.insert_one(log_data)

            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

# Inside the LogSearch class
class LogSearch(Resource):
    def get(self):
        try:
            if 'username' not in session or session.get('role') != 'admin':
                return jsonify({'status': 'error', 'message': 'Unauthorized access'}), 403

            # Extract filters from query parameters
            filters = {
                "level": request.args.get("level"),
                "message": request.args.get("message"),
                "resourceId": request.args.get("resourceId"),
                "traceId": request.args.get("traceId"),
                "spanId": request.args.get("spanId"),
                "commit": request.args.get("commit"),
                "metadata.parentResourceId": request.args.get("metadata.parentResourceId"),
            }

            # Filter logs within a specific date range
            start_date = request.args.get("start_date")
            end_date = request.args.get("end_date")
            if start_date and end_date:
                start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
                end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
                filters["timestamp"] = {"$gte": start_date_dt, "$lt": end_date_dt}

            # Build MongoDB query based on filters
            mongo_query = {key: {"$regex": re.compile(value)} if key != "timestamp" else value for key, value in filters.items() if value}

            # Search logs in MongoDB
            result = list(log_collection.find(mongo_query))

            # Convert ObjectId to string and datetime to string for JSON serialization
            for log in result:
                log['_id'] = str(log['_id'])
                log['timestamp'] = log['timestamp'].strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Return JSON response with logs
            return jsonify({'status': 'success', 'logs': result})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
        
api.add_resource(LogIngestor, '/ingest')
api.add_resource(LogSearch, '/search-logs')

# Session secret key for secure session handling
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('query_interface'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check credentials against the SQLite database
    db = get_db()
    user_data = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    if user_data and hashlib.sha256(password.encode()).hexdigest() == user_data[2]:
        session['username'] = user_data[1]
        session['role'] = user_data[3]
        return redirect(url_for('query_interface'))
    else:
        return render_template('index.html', error='Invalid credentials')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))
    
@app.route('/query_interface')
def query_interface():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))

    return render_template('query_interface.html')

if __name__ == '__main__':
    app.run(port=3000)