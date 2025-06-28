from flask import request, jsonify
from models.salesteam_model import SalesTeam
from utils.auth_utils import hash_password, check_password, generate_salesteam_jwt
from pymongo.errors import PyMongoError

class SalesteamAuthController:
    
    @staticmethod
    def register():
        try:
            data = request.json

            # Check if required fields are provided
            if not data or "email" not in data or "password" not in data:
                return jsonify({"error": "Email and password are required"}), 400

            # Check if a user with this email already exists
            existing = SalesTeam.find_by_email(data.get("email"))
            if existing:
                return jsonify({"error": "Email already exists"}), 400

            # Hash the password before saving
            data["password"] = hash_password(data["password"])

            # Create the new salesman document in the database
            new_id = SalesTeam.create(data)

            return jsonify({"message": "Salesman registered", "id": new_id}), 201

        except PyMongoError as e:
            # Handle database-related errors
            return jsonify({"error": "Database error", "details": str(e)}), 500
        except Exception as e:
            # Handle any other unexpected errors
            return jsonify({"error": "Unexpected error", "details": str(e)}), 500

    @staticmethod
    def login():
        try:
            data = request.json

            # Check if email and password are provided
            if not data or "email" not in data or "password" not in data:
                return jsonify({"error": "Email and password are required"}), 400

            # Look up the user by email
            user = SalesTeam.find_by_email(data.get("email"))
            if not user:
                return jsonify({"error": "Invalid credentials"}), 401

            # Verify the password
            if not check_password(data.get("password"), user["password"]):
                return jsonify({"error": "Invalid credentials"}), 401

            # Generate JWT token upon successful authentication
            token = generate_salesteam_jwt(str(user["_id"]))
            return jsonify({"token": token}), 200

        except PyMongoError as e:
            return jsonify({"error": "Database error", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Unexpected error", "details": str(e)}), 500
