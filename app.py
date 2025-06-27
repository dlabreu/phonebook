from flask import Flask, jsonify

app = Flask(__name__)

contacts = [
    {"id": 1, "name": "Alice Smith", "phone": "+123456789"},
    {"id": 2, "name": "Bob Johnson", "phone": "+987654321"},
    {"id": 3, "name": "Carol Lee", "phone": "+192837465"}
]

@app.route("/api/contacts")
def get_contacts():
    return jsonify(contacts)

@app.route("/")
def home():
    html = "<h1>Simple Phone Book</h1><ul>"
    for c in contacts:
        html += f"<li>{c['name']}: {c['phone']}</li>"
    html += "</ul>"
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
