# This is conceptual Python Flask backend code.
# You would need to install Flask, psycopg2 (for PostgreSQL interaction), and potentially python-dotenv for environment variables.
# This code is for demonstration and needs to be run in a separate environment (e.g., your local machine or a server).

from flask import Flask, request, jsonify
from flask_cors import CORS # To handle Cross-Origin Resource Sharing
import psycopg2 # PostgreSQL adapter
import os

app = Flask(__name__)
CORS(app) # Enable CORS for all routes (important for frontend communication)

# --- Database Connection Configuration ---
# In a real application, you would load these from environment variables
# For example, using python-dotenv:
# from dotenv import load_dotenv
# load_dotenv()
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'phonebook_db')
DB_USER = os.getenv('DB_USER', 'your_username')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
DB_PORT = os.getenv('DB_PORT', '5432')

# Function to get a database connection
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        # In a production app, you'd log this error and handle it more gracefully
        return None

# --- Database Schema Setup (Run this once manually or in a migration script) ---
# You can run this SQL command in your PostgreSQL client (e.g., psql) to create the table:
# CREATE TABLE contacts (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     surname VARCHAR(100),
#     company VARCHAR(100),
#     phone VARCHAR(50) NOT NULL,
#     address TEXT
# );

# --- API Endpoints ---

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, surname, company, phone, address FROM contacts ORDER BY name, surname;")
        contacts_data = cur.fetchall()
        # Convert list of tuples to list of dictionaries for JSON response
        contacts_list = []
        for contact in contacts_data:
            contacts_list.append({
                "id": contact[0],
                "name": contact[1],
                "surname": contact[2],
                "company": contact[3],
                "phone": contact[4],
                "address": contact[5],
            })
        return jsonify(contacts_list)
    except Exception as e:
        print(f"Error fetching contacts: {e}")
        return jsonify({"error": "Failed to fetch contacts"}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    new_contact = request.json
    name = new_contact.get('name')
    surname = new_contact.get('surname')
    company = new_contact.get('company')
    phone = new_contact.get('phone')
    address = new_contact.get('address')

    if not name or not phone:
        return jsonify({"error": "Name and phone are required"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO contacts (name, surname, company, phone, address) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (name, surname, company, phone, address)
        )
        contact_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"message": "Contact added successfully", "id": contact_id}), 201
    except Exception as e:
        conn.rollback() # Rollback on error
        print(f"Error adding contact: {e}")
        return jsonify({"error": "Failed to add contact"}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    updated_data = request.json
    name = updated_data.get('name')
    surname = updated_data.get('surname')
    company = updated_data.get('company')
    phone = updated_data.get('phone')
    address = updated_data.get('address')

    if not name or not phone:
        return jsonify({"error": "Name and phone are required"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE contacts SET name=%s, surname=%s, company=%s, phone=%s, address=%s WHERE id=%s;",
            (name, surname, company, phone, address, contact_id)
        )
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({"error": "Contact not found"}), 404
        return jsonify({"message": "Contact updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        print(f"Error updating contact: {e}")
        return jsonify({"error": "Failed to update contact"}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM contacts WHERE id=%s;", (contact_id,))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({"error": "Contact not found"}), 404
        return jsonify({"message": "Contact deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        print(f"Error deleting contact: {e}")
        return jsonify({"error": "Failed to delete contact"}), 500
    finally:
        cur.close()
        conn.close()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) # Run on port 5000

