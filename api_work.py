from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from marshmallow import ValidationError
from schemas import UserSchema  # Import the schema

app = Flask(__name__)

# MongoDB connection
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["task"]
collection = db["users"]

# Create an instance of UserSchema
user_schema = UserSchema()

# POST: Add a new user
@app.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()  # Get JSON data from the request body
        # Validate and deserialize the input data
        validated_data = user_schema.load(data)
        result = collection.insert_one(validated_data)  # Insert into MongoDB
        return jsonify({"message": "User added successfully", "user_id": str(result.inserted_id)}), 201
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400  # Return validation errors
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET: Retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = list(collection.find({}, {"_id": 0}))  # Exclude the ObjectId from response
        return jsonify({"users": users}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT: Update an existing user by ID
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        # Validate and deserialize the input data
        validated_data = user_schema.load(data)
        result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": validated_data})

        if result.matched_count == 0:
            return jsonify({"message": "User not found"}), 404

        return jsonify({"message": "User updated successfully"}), 200
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE: Remove a user by ID
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        result = collection.delete_one({"_id": ObjectId(user_id)})

        if result.deleted_count == 0:
            return jsonify({"message": "User not found"}), 404

        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
