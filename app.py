from flask import Flask, render_template_string
from prometheus_client import make_wsgi_app, Counter
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

# Track how many people visit the page
# This creates a metric called 'web_visitor_total'
VISITOR_COUNTER = Counter('web_visitor_total', 'Total number of visitors to the DevOps Journey page')

# Light-themed HTML Template (Your existing design)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kartikey DevOps Journey</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --primary: #3b82f6;
            --accent: #10b981;
        }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        header {
            width: 100%;
            padding: 4rem 0;
            background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%);
            border-bottom: 1px solid #e2e8f0;
            text-align: center;
        }
        .container {
            max-width: 800px;
            width: 90%;
            margin-top: -3rem;
        }
        .card {
            background: var(--card-bg);
            padding: 2.5rem;
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        h1 { font-size: 2.5rem; margin-bottom: 0.5rem; color: var(--text); }
        h2 { color: var(--primary); border-bottom: 2px solid #f1f5f9; padding-bottom: 0.5rem; }
        .badge {
            display: inline-block;
            background: #dcfce7;
            color: #166534;
            padding: 0.25rem 0.75rem;
            border-radius: 99px;
            font-size: 0.875rem;
            font-weight: 600;
        }
        .journey-log {
            list-style: none;
            padding: 0;
        }
        .log-item {
            padding: 1rem;
            border-left: 4px solid var(--primary);
            background: #f1f5f9;
            margin-bottom: 1rem;
            border-radius: 0 8px 8px 0;
        }
        footer {
            margin-top: 2rem;
            color: #64748b;
            font-size: 0.875rem;
            padding-bottom: 2rem;
        }
    </style>
</head>
<body>
    <header>
        <h1>Kartikey's DevOps Journey</h1>
        <p>Documenting the path to SRE & Infrastructure Excellence</p>
    </header>

    <div class="container">
        <div class="card">
            <h2>Current Project Status <span class="badge">Live</span></h2>
            <p><strong>Environment:</strong> AWS EC2 (t3.micro)</p>
            <p><strong>Deployment:</strong> Automated via GitHub Actions & Docker Hub</p>
            <p><strong>Observability:</strong> Prometheus Exporter Integrated</p>
        </div>

        <div class="card">
            <h2>Milestones Reached</h2>
            <ul class="journey-log">
                <li class="log-item">
                    <strong>Containerization Mastered:</strong> Built a multi-stage Dockerfile for Flask optimization.
                </li>
                <li class="log-item">
                    <strong>CI/CD Implementation:</strong> Automated the build-test-deploy cycle using GitHub Workflows.
                </li>
                <li class="log-item">
                    <strong>Observability Setup:</strong> Integrated Prometheus metrics for real-time traffic tracking.
                </li>
            </ul>
        </div>
    </div>

    <footer>
        &copy; 2026 Kartikey | Built with Flask & GitHub Actions
    </footer>
</body>
</html>
"""

@app.route('/')
def home():
    VISITOR_COUNTER.inc() # Increment the metric count
    return render_template_string(HTML_TEMPLATE)

# This is the "Magic" step: 
# It adds a /metrics page that Prometheus will scrape forr data
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    # Running on 5000 as usual
    app.run(host='0.0.0.0', port=5000)