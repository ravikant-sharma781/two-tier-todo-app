from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os
import time

app = Flask(__name__)
CORS(app)

# =========================
# MongoDB Connection
# =========================

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

for i in range(5):
    try:
        client = MongoClient(mongo_uri)
        client.server_info()  # Force connection
        print("Connected to MongoDB")
        break
    except Exception as e:
        print("Waiting for MongoDB...", e)
        time.sleep(2)

db = client["todo_db"]
collection = db["tasks"]

# =========================
# Health Check
# =========================

@app.route('/')
def home():
    return "Backend is running"

# =========================
# CREATE Task
# =========================

@app.route('/tasks', methods=['POST'])
def add_task():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Text is required"}), 400

        result = collection.insert_one({
            "text": data["text"]
        })

        return jsonify({
            "id": str(result.inserted_id),
            "text": data["text"]
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================
# READ Tasks
# =========================

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = []

        for task in collection.find():
            tasks.append({
                "id": str(task["_id"]),
                "text": task["text"]
            })

        return jsonify(tasks)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================
# DELETE Task
# =========================

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            return jsonify({"error": "Task not found"}), 404

        return jsonify({"message": "Task deleted"})

    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400

# =========================
# Run App
# =========================

if __name__ == '__main__':
    app.run(
        debug=False,
        host='0.0.0.0',
        port=5000
    )
