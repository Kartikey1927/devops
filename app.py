from flask import Flask, Response, request, render_template_string
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import psycopg2
import os
import time

app = Flask(__name__)

# --- Configuration (SRE: Use Environment Variables for Security) ---
DB_HOST = os.getenv("DB_HOST", "172.31.33.189")
DB_NAME = os.getenv("DB_NAME", "wine_cellar_db")
DB_USER = os.getenv("DB_USER", "kartikey")
DB_PASS = os.getenv("DB_PASS", "devops_pass")

# --- Prometheus Metrics (SRE: Observability) ---
REQUEST_COUNT = Counter('lacantina_requests_total', 'Total La Cantina Visits', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('lacantina_request_latency_seconds', 'Time spent processing request')

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, 
            database=DB_NAME, 
            user=DB_USER, 
            password=DB_PASS, 
            connect_timeout=3
        )
        return conn
    except Exception as e:
        print(f"SRE Alert: Database connection failed: {e}")
        return None

@app.route('/')
def home():
    start_time = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    
    conn = get_db_connection()
    total_sales_sim = 0
    db_status = "Cloud DB: Disconnected ❌"
    db_color = "#e74c3c"

    if conn:
        try:
            cur = conn.cursor()
            # Log the visitor in our distributed database
            cur.execute("INSERT INTO shop_visits (visitor_ip) VALUES (%s);", (request.remote_addr or 'Internal',))
            conn.commit()
            
            # Fetch total visitor count
            cur.execute("SELECT COUNT(*) FROM shop_visits;")
            total_sales_sim = cur.fetchone()[0]
            
            cur.close()
            conn.close()
            db_status = "Cloud DB: Syncing ✅"
            db_color = "#27ae60"
        except Exception as e:
            db_status = f"Data Error: {e}"

    # Track how long the page took to render
    REQUEST_LATENCY.observe(time.time() - start_time)

    return render_template_string(HTML_TEMPLATE, db_status=db_status, db_color=db_color, visits=total_sales_sim)

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# --- Premium UI Template ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>LA CANTINA | SRE Dashboard</title>
    <style>
        :root { --main-bg: #121212; --accent: #d35400; --glass: rgba(255, 255, 255, 0.05); }
        body { background: var(--main-bg); color: #e0e0e0; font-family: 'Georgia', serif; margin: 0; padding: 0; }
        .hero { height: 60vh; background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=1500&q=80'); background-size: cover; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
        .nav-bar { background: #0a0a0a; padding: 15px 50px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--accent); }
        .status-pill { background: {{ db_color }}; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8em; font-family: monospace; }
        .content { max-width: 1000px; margin: -50px auto 50px; background: #1a1a1a; padding: 40px; border-radius: 10px; border: 1px solid #2c3e50; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 30px; }
        .card { background: var(--glass); padding: 20px; border-radius: 8px; text-align: center; border: 1px solid transparent; transition: 0.3s; }
        .card:hover { border-color: var(--accent); transform: translateY(-5px); }
        h1 { font-size: 4em; margin: 0; color: var(--accent); letter-spacing: 2px; }
        .footer { text-align: center; padding: 20px; font-size: 0.8em; color: #555; }
    </style>
</head>
<body>
    <div class="nav-bar">
        <div style="color: var(--accent); font-weight: bold; font-size: 1.4em; letter-spacing: 1px;">LA CANTINA</div>
        <div class="status-pill">{{ db_status }}</div>
    </div>

    <div class="hero">
        <h1>LA CANTINA</h1>
        <p style="font-size: 1.2em; color: #bdc3c7;">Premium Distributed Distillery & Lounge</p>
    </div>

    <div class="content">
        <div style="text-align: center; margin-bottom: 40px;">
            <p style="font-size: 1.2em;">Total Guests Logged in PostgreSQL: <b style="color: var(--accent);">{{ visits }}</b></p>
            <hr style="border: 0; border-top: 1px solid #2c3e50; width: 50%;">
        </div>

        <div class="grid">
            <div class="card">
                <h3 style="color: var(--accent);">VPC Private Lounge</h3>
                <p>Isolated networking, exclusive access.</p>
            </div>
            <div class="card">
                <h3 style="color: var(--accent);">Kubernetes Agave</h3>
                <p>Auto-scaling barrels, crisp reliability.</p>
            </div>
            <div class="card">
                <h3 style="color: var(--accent);">Prometheus Proof</h3>
                <p>Rich monitoring, deep telemetry insights.</p>
            </div>
        </div>
    </div>

    <div class="footer">
        Infrastructure as Code | <a href="/metrics" style="color: var(--accent); text-decoration: none;">Live Metrics Data</a>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)