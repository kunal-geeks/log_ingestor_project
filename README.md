# Log Ingestor and Query Interface

## Overview

This project implements a log ingestor system and a query interface for handling log data efficiently. The system is built using Flask for the log ingestor, MongoDB Atlas for storage, and includes a sample data populator and query tester.

## Prerequisites

- Python 3.7+
- MongoDB Atlas connection string
- Flask
- Flask-PyMongo
- Flask-RESTful
- VS Code
- sqlite3

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/kunal-geeks/log_ingestor_project.git
   ```

2. Navigate to the project directory:

   ```bash
   cd log_ingestor_project
   ```

   - open bash terminal in the project directory and run the following commands:

   ```bash
   export FLASK_APP=log_ingestor
   ```

3. Initiate the database and get admin credentials as only admin can perform query operations and log ingestion.I am using sqlite db for storing user information or structured data.:

   ```bash
   init-db
   ```

   - you test admin credential will be following so use it login and perform query operations.:

   - username : admin
   - password : admin_password

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. create a .env folder in the root directory and add the following:

   - MONGODB_URI='your_mongoDB_connection_string'
   - FLASK_SECRET_KEY="your_secret_key"

Make sure MongoDB is running and is used to store unstructured logs data in Atlas.

5. Open a new terminal window and run the populate_logs.py:

   ```bash
   python populate_logs.py
   ```

This script populates the collection named "logs_data" in the database named "logs" in the mongo Atlas with sample log data.

6. Run the command to start the server:

   ```bash
   python log_ingestor.py
   ```

## Sample Queries
   
1. Find all logs with the level set to 'error'.
2. Search for logs with the message containing the term 'Failed to connect'.
3. Retrieve all logs related to resourceId 'server-1234'.
4. Filter logs between the timestamp '2023-09-10T00:00:00Z' and '2023-09-15T23:59:59Z'.

## Optional: System design preview
- [https://whimsical.com/system-design-for-logs-ingestion-6CNFZa1DFKMfFpVUZw6mmH]

## Submission
- Submit your assignment through the provided GitHub Classroom link.

- For any issues or questions, please reach out to [kunal.ucet@gmail.com].
