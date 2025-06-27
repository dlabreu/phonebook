from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Dummy data that matches the expected format from your React app
contacts = [
    {"id": 1, "name": "Alice Smith", "phone": "+123456789"},
    {"id": 2, "name": "Bob Johnson", "phone": "+987654321"},
    {"id": 3, "name": "Carol Lee", "phone": "+192837465"}
]

@app.route("/api/contacts", methods=["GET"])
def get_contacts():
    return jsonify(contacts)

# Optional: Add a health check route
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # Get the port from the environment (useful for OpenShift)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
