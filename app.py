from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# DB config from environment
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "phonebook_db")
DB_USER = os.environ.get("DB_USER", "your_username")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "your_password")
DB_PORT = os.environ.get("DB_PORT", "5432")

# Connect to DB
def get_conn():
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD,
        port=DB_PORT
    )

# Simple HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Phone Book</title>
</head>
<body>
    <h1>📖 Contact List</h1>
    <form method="post" action="/add">
        <input name="name" placeholder="Name" required>
        <input name="surname" placeholder="Surname">
        <input name="company" placeholder="Company">
        <input name="phone" placeholder="Phone" required>
        <input name="address" placeholder="Address">
        <button type="submit">Add</button>
    </form>
    <ul>
    {% for c in contacts %}
        <li>
            {{ c[1] }} {{ c[2] }} ({{ c[3] }}) - {{ c[4] }} | {{ c[5] }}
            <form method="post" action="/delete/{{ c[0] }}" style="display:inline;">
                <button type="submit">Delete</button>
            </form>
        </li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/")
def home():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM contacts ORDER BY id")
            contacts = cur.fetchall()
    return render_template_string(HTML_TEMPLATE, contacts=contacts)

@app.route("/add", methods=["POST"])
def add_contact():
    fields = ["name", "surname", "company", "phone", "address"]
    data = [request.form.get(f, '') for f in fields]
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO contacts (name, surname, company, phone, address)
                VALUES (%s, %s, %s, %s, %s)
            """, data)
            conn.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
            conn.commit()
    return redirect(url_for("home"))

@app.route("/api/contacts", methods=["GET"])
def get_contacts():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM contacts ORDER BY id")
            rows = cur.fetchall()
    return jsonify([
        {
            "id": row[0],
            "name": row[1],
            "surname": row[2],
            "company": row[3],
            "phone": row[4],
            "address": row[5],
        }
        for row in rows
    ])

@app.route("/api/contacts", methods=["POST"])
def api_add():
    data = request.get_json()
    if not data or 'name' not in data or 'phone' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    values = [data.get(f, '') for f in ['name', 'surname', 'company', 'phone', 'address']]
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO contacts (name, surname, company, phone, address)
                VALUES (%s, %s, %s, %s, %s)
            """, values)
            conn.commit()
    return jsonify({"message": "Contact added"}), 201

@app.route("/api/contacts/<int:contact_id>", methods=["DELETE"])
def api_delete(contact_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
            conn.commit()
    return jsonify({"message": "Contact deleted"}), 200

@app.route("/health")
def health():
    return jsonify({"status": "ok"})
