from flask import Flask, Response, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import psycopg2
import os

app = Flask(__name__)

# --- Configuration ---
DB_HOST = "172.31.33.189" 
DB_NAME = "journey_db"
DB_USER = "kartikey"
DB_PASS = "devops_pass"

# --- Prometheus Metrics ---
REQUEST_COUNT = Counter('kartikey_devops_requests_total', 'Total HTTP Requests')

def get_db_connection():
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, connect_timeout=5)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

@app.route('/')
def hello_world():
    REQUEST_COUNT.inc()
    conn = get_db_connection()
    total_visits = 0
    db_status = "Disconnected ❌"

    if conn:
        try:
            cur = conn.cursor()
            # 1. Log the current visit
            cur.execute("INSERT INTO visits (visitor_ip) VALUES (%s);", (request.remote_addr or 'Internal',))
            conn.commit()
            
            # 2. Fetch the total count from the Data Node
            cur.execute("SELECT COUNT(*) FROM visits;")
            total_visits = cur.fetchone()[0]
            
            cur.close()
            conn.close()
            db_status = "Connected & Syncing ✅"
        except Exception as e:
            db_status = f"Data Error: {e}"

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Kartikey's DevOps Roadmap</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; max-width: 900px; margin: 40px auto; background-color: #f4f7f9; color: #2c3e50; line-height: 1.6; }}
            .container {{ background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }}
            .header {{ text-align: center; border-bottom: 2px solid #eee; padding-bottom: 20px; margin-bottom: 30px; }}
            .status-bar {{ background: #2d3436; color: #00cec9; padding: 10px 20px; border-radius: 8px; font-family: monospace; margin-bottom: 30px; display: flex; justify-content: space-between; }}
            
            .section {{ margin-bottom: 25px; padding: 20px; border-radius: 10px; border-left: 6px solid #dfe6e9; background: #fff; transition: 0.3s; }}
            .completed {{ border-left-color: #00b894; background: #f0fff4; }}
            .current {{ border-left-color: #0984e3; background: #ebf5ff; box-shadow: 0 4px 12px rgba(9,132,227,0.1); }}
            .future {{ border-left-color: #b2bec3; opacity: 0.7; }}
            
            h2 {{ margin-top: 0; color: #2d3436; }}
            .badge {{ font-size: 0.7em; padding: 4px 8px; border-radius: 4px; text-transform: uppercase; vertical-align: middle; margin-left: 10px; }}
            .badge-done {{ background: #00b894; color: white; }}
            .badge-now {{ background: #0984e3; color: white; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 DevOps Engineering Track</h1>
                <p>Student: <b>Kartikey</b> | Level: <b>Distributed Systems</b></p>
            </div>

            <div class="status-bar">
                <span>DATABASE: {db_status}</span>
                <span>TOTAL VISITS LOGGED: {total_visits}</span>
            </div>

            <div class="section completed">
                <h2>1. Monolithic Beginnings <span class="badge badge-done">Completed</span></h2>
                <ul>
                    <li>Set up first EC2 Instance on AWS (App Node).</li>
                    <li>Automated deployments using <b>GitHub Actions</b> (CI/CD).</li>
                    <li>Integrated <b>Prometheus</b> for real-time metric tracking.</li>
                </ul>
            </div>

            <div class="section current">
                <h2>2. Distributed Architecture <span class="badge badge-now">In Progress</span></h2>
                <ul>
                    <li>Provisioned a dedicated <b>Data Node</b> (Instance 2).</li>
                    <li>Deployed <b>PostgreSQL</b> inside a Docker container.</li>
                    <li>Established secure <b>Private Networking</b> between instances.</li>
                    <li>Implemented <b>Stateful Persistence</b> (Logging visits to DB).</li>
                </ul>
            </div>

            <div class="section future">
                <h2>3. Cloud Native & Kubernetes <span class="badge">Up Next</span></h2>
                <ul>
                    <li>Containerizing the entire stack with Docker Compose.</li>
                    <li>Migrating to <b>Kubernetes (EKS)</b> for auto-scaling.</li>
                    <li>Setting up <b>Grafana Dashboards</b> for visual monitoring.</li>
                </ul>
            </div>

            <div style="text-align: center; margin-top: 30px; font-size: 0.9em;">
                <a href="/metrics" style="color: #0984e3; text-decoration: none;">View Raw Prometheus Metrics →</a>
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