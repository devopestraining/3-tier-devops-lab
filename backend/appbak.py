import os
from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

def db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "database"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "devopsdb"),
        user=os.getenv("DB_USER", "devops"),
        password=os.getenv("DB_PASSWORD", "devopspass")
    )

@app.get("/")
def home():
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT message FROM demo LIMIT 1")
        row = cur.fetchone()
        cur.close()
        conn.close()

        return jsonify({
            "application": "3-Tier DevOps Demo",
            "status": "success",
            "message_from_database": row[0] if row else "No data",
            "architecture": "Nginx -> Flask -> MySQL"
        })
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)}), 500

@app.get("/health")
def health():
    return jsonify({"status": "healthy"})

@app.get("/db-test")
def db_test():
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({"database": "reachable", "result": result})
    except Exception as exc:
        return jsonify({"database": "unreachable", "error": str(exc)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
