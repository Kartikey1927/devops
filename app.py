from flask import Flask, jsonify

# This line starts our web application
app = Flask(__name__)

# This is the 'Home Page' - what you see at http://localhost:5000/
@app.route("/")
def home():
    return jsonify({"message": "My first DevOps pipeline is working!"})

# This is a 'Health Check' - it tells the cloud 'I am still running!'
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)