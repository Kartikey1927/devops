from flask import Flask, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Day 2: Prometheus Metrics Setup
# This creates a 'counter' that tracks how many times the page is loaded.
REQUEST_COUNT = Counter(
    'kartikey_devops_requests_total', 
    'Total HTTP Requests tracked for Kartikey'
)

@app.route('/')
def hello_world():
    # Increment the counter every time this function is called
    REQUEST_COUNT.inc()
    
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kartikey's DevOps Journey</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 40px auto; padding: 20px; background-color: #f0f2f5; }
            .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h1 { color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 10px; }
            .day-card { margin-top: 20px; padding: 15px; border-left: 5px solid #1a73e8; background: #e8f0fe; border-radius: 4px; }
            .day-card.active { border-left-color: #34a853; background: #e6f4ea; }
            ul { padding-left: 20px; }
            li { margin-bottom: 8px; }
            .footer { margin-top: 30px; font-size: 0.85em; color: #666; text-align: center; }
            a { color: #1a73e8; text-decoration: none; font-weight: bold; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Kartikey's DevOps Journey</h1>
            <p>Tracking the evolution from local code to automated cloud infrastructure.</p>

            <div class="day-card">
                <h3>✅ Day 1: The Foundation</h3>
                <ul>
                    <li><b>Compute:</b> AWS EC2 Instance (Ubuntu)</li>
                    <li><b>Docker:</b> Containerization of Flask App</li>
                    <li><b>Orchestration:</b> Multi-container setup with Docker Compose</li>
                    <li><b>CI/CD:</b> GitHub Actions for automated deployment</li>
                </ul>
            </div>

            <div class="day-card active">
                <h3>🔥 Day 2: Reliability & Observability</h3>
                <ul>
                    <li><b>Networking:</b> Permanent AWS Elastic IP (13.62.12.82)</li>
                    <li><b>Monitoring:</b> Prometheus Scraping & Metrics Collection</li>
                    <li><b>Visualization:</b> Grafana Dashboarding</li>
                    <li><b>Persistence:</b> Docker <code>restart: always</code> for self-healing</li>
                </ul>
            </div>

            <div class="footer">
                Live Monitoring: 
                <a href="http://13.62.12.82:9090" target="_blank">Prometheus</a> | 
                <a href="http://13.62.12.82:3000" target="_blank">Grafana</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/metrics')
def metrics():
    # This endpoint is specifically for Prometheus to "scrape" the data.
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    # Binding to 0.0.0.0 allows the EC2 public IP to access the app
    app.run(host='0.0.0.0', port=5000)