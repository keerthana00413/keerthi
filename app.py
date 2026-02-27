from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash
import sqlite3
import flask
import flask_cors
import werkzeug

app = Flask(__name__)
CORS(app)  # Allow frontend connection

# -------------------------
# Database Setup
# -------------------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------------
# Register Route
# -------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    if len(username) < 8:
        return jsonify({"message": "Username must be at least 8 characters"}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        """, (username, email, hashed_password))

        conn.commit()
        conn.close()

        return jsonify({"message": "Registration successful!"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"message": "Email already exists"}), 400

    except Exception as e:
        return jsonify({"message": "Server error"}), 500


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)