import os
import json
import requests
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# Build connector JSON in memory
# -----------------------------
connector_config = {
    "name": "postgres-connector",
    "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "database.hostname": os.getenv("POSTGRES_HOST"),
        "database.port": os.getenv("POSTGRES_PORT"),
        "database.user": os.getenv("POSTGRES_USER"),
        "database.password": os.getenv("POSTGRES_PASSWORD"),
        "database.dbname": os.getenv("POSTGRES_DB"),
        "topic.prefix": "banking_server",
        "table.include.list": "public.customers,public.accounts,public.transactions",
        "plugin.name": "pgoutput",
        "slot.name": "banking_slot",
        "publication.autocreate.mode": "filtered",
        "tombstones.on.delete": "false",
        "decimal.handling.mode": "double",
    },
}

# -----------------------------
# Send request to Debezium Connect
# -----------------------------
url = "http://localhost:8083/connectors"
headers = {"Content-Type": "application/json"}


print("Starting connector creation...", flush=True)

try:
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(connector_config),
        timeout=10
    )

    print("STATUS CODE:", response.status_code, flush=True)
    print("RESPONSE:", response.text, flush=True)

    if response.status_code == 201:
        print("✅ Connector created successfully!", flush=True)

    elif response.status_code == 409:
        print("⚠️ Connector already exists.", flush=True)

    else:
        print(f"❌ Failed: {response.status_code}", flush=True)

except Exception as e:
    print("ERROR:", e, flush=True)