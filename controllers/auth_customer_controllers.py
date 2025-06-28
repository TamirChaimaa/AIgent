from flask import request, jsonify
from flasgger import swag_from
from models.customer_model import Customer
from utils.auth_utils import hash_password, check_password, generate_jwt
import datetime

class AuthController:

    @staticmethod
    @swag_from({
        'tags': ['Authentication Customers'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'firstname': {'type': 'string', 'example': 'John'},
                        'lastname': {'type': 'string', 'example': 'Doe'},
                        'email': {'type': 'string', 'example': 'john@example.com'},
                        'password': {'type': 'string', 'example': 'strongPassword123'},
                        'phone': {'type': 'string', 'example': '+212600000000'}
                    },
                    'required': ['firstname', 'lastname', 'email', 'password']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'User created successfully',
                'examples': {
                    'application/json': {
                        'message': 'User created successfully',
                        'customer_id': '60b8d295f1a4c431d88b4567'
                    }
                }
            },
            400: {'description': 'Missing required fields or Email already exists'},
            500: {'description': 'Signup failed'}
        }
    })
    def signup():
        """
        Handles user registration.
        Validates input, checks for duplicate email,
        hashes the password, saves user to database,
        and returns success or error responses.
        """
        try:
            data = request.json
            required_fields = ['firstname', 'lastname', 'email', 'password']

            if not all(field in data for field in required_fields):
                return jsonify({'message': 'Missing required fields'}), 400

            if Customer.find_by_email(data['email']):
                return jsonify({'message': 'Email already exists'}), 400

            hashed_pw = hash_password(data['password'])

            user_data = {
                'firstname': data['firstname'],
                'lastname': data['lastname'],
                'email': data['email'],
                'phone': data.get('phone', ''),
                'password': hashed_pw,
                'created_at': datetime.datetime.utcnow()
            }

            result = Customer.create(user_data)

            return jsonify({
                'message': 'User created successfully',
                'customer_id': str(result.inserted_id)
            }), 201

        except Exception as e:
            return jsonify({'message': 'Signup failed', 'error': str(e)}), 500


    @staticmethod
    @swag_from({
        'tags': ['Authentication Customers'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'email': {'type': 'string', 'example': 'john@example.com'},
                        'password': {'type': 'string', 'example': 'strongPassword123'}
                    },
                    'required': ['email', 'password']
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Login successful',
                'examples': {
                    'application/json': {
                        'token': 'jwt_token_here',
                        'user': {
                            'id': '60b8d295f1a4c431d88b4567',
                            'firstname': 'John',
                            'lastname': 'Doe',
                            'email': 'john@example.com',
                            'phone': '+212600000000'
                        }
                    }
                }
            },
            400: {'description': 'Email and password are required'},
            401: {'description': 'Invalid email or password'},
            500: {'description': 'Login failed'}
        }
    })
    def login():
        """
        Handles user login.
        Validates input, verifies user existence and password,
        generates JWT token on success,
        and returns user info with token or error responses.
        """
        try:
            data = request.json

            if not data.get('email') or not data.get('password'):
                return jsonify({'message': 'Email and password are required'}), 400

            user = Customer.find_by_email(data['email'])
            if not user:
                return jsonify({'message': 'Invalid email or password'}), 401

            if not check_password(data['password'], user['password']):
                return jsonify({'message': 'Invalid email or password'}), 401

            token = generate_jwt(str(user['_id']))

            return jsonify({
                'token': token,
                'user': {
                    'id': str(user['_id']),
                    'firstname': user['firstname'],
                    'lastname': user['lastname'],
                    'email': user['email'],
                    'phone': user.get('phone', '')
                }
            })

        except Exception as e:
            return jsonify({'message': 'Login failed', 'error': str(e)}), 500
