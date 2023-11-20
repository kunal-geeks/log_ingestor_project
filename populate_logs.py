import requests
from faker import Faker
from datetime import datetime, timedelta
import random
import json

# Set the MongoDB endpoint
INGEST_URL = "http://localhost:3000/ingest"

# Initialize Faker for generating random data
fake = Faker()

# Function to generate random log data
def generate_random_log():
    return {
        "level": random.choice(["info", "warning", "error"]),
        "message": fake.sentence(),
        "resourceId": fake.uuid4(),
        "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "traceId": fake.uuid4(),
        "spanId": fake.uuid4(),
        "commit": fake.sha1(),
        "metadata": {
            "parentResourceId": fake.uuid4()
        }
    }

# Generate and insert 15 random log entries
for _ in range(15):
    log_data = generate_random_log()
    response = requests.post(INGEST_URL, json=log_data)

    if response.status_code == 200:
        print("Log data ingested successfully:", response.json())
    else:
        print("Error ingesting log data:", response.status_code, response.text)
