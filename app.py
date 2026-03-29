from flask import Flask, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import psycopg2
import os

app = Flask(__name__)

# --- Configuration ---
# Replace this with the Private IP of your Instance 2
DB_HOST = "172.31.33.189" 
DB_NAME = "journey_db"
DB_USER = "kartikey"
DB_PASS = "devops_pass"

# --- Prometheus Metrics ---
REQUEST_COUNT = Counter(
    'kartikey_devops_requests_total', 
    'Total HTTP Requests tracked for Kartikey'
)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

@app.route('/')
def hello_world():
    REQUEST_COUNT.inc()
    
    # Try to log the visit in the database
    conn = get_db_connection()
    db_status = "Connected ✅" if conn else "Disconnected ❌"
    if conn:
        conn.close()

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Kartikey's Distributed DevOps Journey</title>
        <style>
            body {{ font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background-color: #f0f2f5; }}
            .container {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .status {{ font-weight: bold; color: {'green' if conn else 'red'}; }}
            .day-card {{ margin-top: 20px; padding: 15px; border-left: 5px solid #1a73e8; background: #e8f0fe; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Kartikey's Distributed Journey</h1>
            <p>Database Status: <span class="status">{db_status}</span></p>
            
            <div class="day-card">
                <h3>✅ Day 2.5: Distributed Architecture</h3>
                <ul>
                    <li><b>App Node:</b> Instance 1 (Elastic IP: 13.62.12.82)</li>
                    <li><b>Data Node:</b> Instance 2 (PostgreSQL Microservice)</li>
                    <li><b>Networking:</b> Private VPC connection on Port 5432</li>
                </ul>
            </div>

            <div style="margin-top:20px; font-size: 0.8em;">
                <a href="/metrics">View Prometheus Metrics</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)