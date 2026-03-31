from flask import Flask, Response, request, render_template_string
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import psycopg2
import os
import time

app = Flask(__name__)

# --- Configuration ---
DB_HOST = os.getenv("DB_HOST", "172.31.33.189") # Your Data Node IP
DB_NAME = "wine_cellar_db"
DB_USER = "kartikey"
DB_PASS = "devops_pass"

# --- Metrics ---
REQUEST_COUNT = Counter('wine_shop_requests_total', 'Total Visits', ['endpoint'])
REQUEST_LATENCY = Histogram('wine_shop_latency_seconds', 'Response Time')

def get_db_connection():
    try:
        return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, connect_timeout=3)
    except:
        return None

@app.route('/')
def home():
    start_time = time.time()
    REQUEST_COUNT.labels(endpoint='/').inc()
    
    conn = get_db_connection()
    visits = 0
    status = "Database Offline ❌"
    color = "#e74c3c"

    if conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO shop_visits (visitor_ip) VALUES (%s);", (request.remote_addr,))
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM shop_visits;")
        visits = cur.fetchone()[0]
        cur.close()
        conn.close()
        status = "Database Syncing ✅"
        color = "#27ae60"

    REQUEST_LATENCY.observe(time.time() - start_time)
    
    # Simple HTML template for testing
    return f"""
    <body style="background:#1a1a1a; color:white; text-align:center; padding-top:100px;">
        <h1 style="color:#c5a059;">Kartikey's Wine Cellar</h1>
        <div style="background:{color}; display:inline-block; padding:10px; border-radius:5px;">{status}</div>
        <h2>Total Bottles Logged: {visits}</h2>
        <a href="/metrics" style="color:gold;">View Prometheus Metrics</a>
    </body>
    """

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)