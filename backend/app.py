from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient("mongodb://db:27017/")
db = client["todo_db"]
collection = db["tasks"]

# CREATE task
@app.route('/tasks', methods=['POST'])
def add_task():
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

# READ tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = []

    for task in collection.find():
        tasks.append({
            "id": str(task["_id"]),
            "text": task["text"]
        })

    return jsonify(tasks)

# DELETE task
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Task deleted"})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
