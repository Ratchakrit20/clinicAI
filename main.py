from dotenv import load_dotenv
from os import getenv, path
import cv2
from flask import Flask, request, jsonify
from http.client import OK, BAD_REQUEST, INTERNAL_SERVER_ERROR
from db import get_mongo_collection

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

collection = get_mongo_collection()

# Define routes
@app.route('/')
def index():
    return 'Welcome to your Flask app!'

@app.route('/hello', methods=['GET'])
def hello():
    name = request.args.get('name') 
    if name is None or name == "":
        return jsonify({"message" : "invalid request" , "data" : None}), BAD_REQUEST
    res = jsonify({"message" : "success", "data" : name}), OK
    return res


# @app.route('/user', methods=['POST'])
# def post_user():
#     name = request.args.get('name')
#     try:
#         existing_user = collection.find_one({"name": name})
        

#         # Process the POST operation as needed
#         # You may want to insert the user into the database or perform other actions

#         return jsonify({"message": "User created successfully", "data": existing_user}), OK
#     except Exception as e:
#         return jsonify({"message": f"Error: {str(e)}", "data": None}), INTERNAL_SERVER_ERROR


@app.route('/user', methods=["POST"])
def create_user():
    try:
        data = request.json

        if not isinstance(data, list):
            return jsonify({"message": "Invalid request format. Expecting a list of users.", "data": None}), BAD_REQUEST

        created_users = []

        for user_data in data:
            name = user_data.get('name')

            if name is None or name == "":
                return jsonify({"message": "Invalid request. Each user must have a 'name' field.", "data": None}), BAD_REQUEST

            # Check if the user already exists in the database
            existing_user = collection.find_one({"name": name})

            if existing_user:
                created_users.append({"name": name, "message": "User already exists", "data": existing_user})
            else:
                # If the user does not exist, insert a new record
                result = collection.insert_one({"name": name})

                # Check if the insertion was successful
                if result.inserted_id:
                    created_users.append({"name": name, "message": "User created successfully"})
                else:
                    return jsonify({"message": "Failed to create user", "data": None}), INTERNAL_SERVER_ERROR

        return jsonify({"message": "Users created successfully", "data": created_users}), OK

    except Exception as e:
        return jsonify({"error": str(e)}), INTERNAL_SERVER_ERROR


@app.route('/user', methods=['PUT'])
def put_user():
    name = request.args.get('name')

    if name is None or name == "":
        return jsonify({"message": "Invalid request", "data": None}), BAD_REQUEST

    try:
        # Check if the user already exists in the database
        existing_user = collection.find_one({"name": name})

        if existing_user:
            # User exists, you may want to update the existing data here
            # For now, let's just return a message without updating
            return jsonify({"message": "User already exists", "data": existing_user}), OK
        else:
            # If the user does not exist, insert a new record
            result = collection.insert_one({"name": name})

            # Check if the insertion was successful
            if result.inserted_id:
                return jsonify({"message": "User inserted successfully", "data": name}), OK
            else:
                return jsonify({"message": "Failed to insert user", "data": None}), INTERNAL_SERVER_ERROR

    except Exception as e:
        return jsonify({"error": str(e)}), INTERNAL_SERVER_ERROR
    
@app.route('/user', methods=["DELETE"])
def delete_user():
    name = request.args.get('name')

    if name is None or name == "":
        return jsonify({"message": "Invalid request", "data": None}), BAD_REQUEST

    try:
        # Check if the user exists in the database
        existing_user = collection.find_one({"name": name})

        if existing_user:
            # If the user exists, delete the record
            collection.delete_one({"name": name})
            return jsonify({"message": "User deleted successfully", "data": name}), OK
        else:
            return jsonify({"message": "User not found", "data": None}), BAD_REQUEST

    except Exception as e:
        return jsonify({"error": str(e)}), INTERNAL_SERVER_ERROR
    





# Additional routes can be added based on your requirements

if __name__ == '__main__':
    app.run(debug=True)