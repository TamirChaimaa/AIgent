from http.client import UNAUTHORIZED
import os
import bcrypt
from bson import ObjectId
from flask import request
import jwt
import datetime
from dotenv import load_dotenv
from werkzeug.exceptions import Unauthorized
from bson import ObjectId

from models.customer_model import Customer

# Load environment variables from .env file
load_dotenv()

# Retrieve the secret key used for JWT encoding/decoding
SECRET_KEY = os.getenv("SECRET_KEY")


# -------- Password Hashing --------
def hash_password(password: str) -> bytes:
    """
    Hashes a plain text password using bcrypt and returns the hashed version.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(password: str, hashed: bytes) -> bool:
    """
    Compares a plain text password with a hashed password.
    Returns True if they match, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


# -------- JWT Token Handling --------
def generate_jwt(customer_id: str) -> str:
    """
    Generates a JWT token for the given user ID.
    The token includes:
      - 'customer_id': The ID of the authenticated user
      - 'exp': Expiration time (24 hours from generation)
    Returns the encoded JWT token as a string.
    """
    payload = {
        'customer_id': customer_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def generate_salesteam_jwt(salesteam_id: str) -> str:
    """
    Generates a JWT token for the given sales team member ID.
    The token includes:
      - 'salesteam_id': The ID of the authenticated sales team member
      - 'exp': Expiration time (24 hours from generation)
    Returns the encoded JWT token as a string.
    """
    payload = {
        'salesteam_id': salesteam_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def decode_jwt(token: str):
    """
    Decodes a JWT token using the secret key and validates its signature.
    Returns the decoded payload (e.g., customer_id).
    Raises jwt.ExpiredSignatureError or jwt.InvalidTokenError if invalid.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

def get_customer_id_from_token(expected_id=None):
    """
    Extracts the JWT token from the Authorization header,
    decodes it using the secret key,
    retrieves the customer ID from the payload,
    verifies that the user exists,
    and optionally checks if the token belongs to the expected user.

    Args:
        expected_id (str, optional): ID to compare against the token's user ID.

    Returns:
        dict: The user object if the token is valid and the user exists.

    Raises:
        Unauthorized: If the token is missing, invalid, expired, or does not match the expected user.
    """
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise Unauthorized("Authorization header is missing")

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise Unauthorized("Authorization header must be in 'Bearer <token>' format")

    token = parts[1]
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        customer_id = payload.get('customer_id')

        if not customer_id:
            raise Unauthorized("Token payload is missing 'customer_id'")
        
        customer_id = ObjectId(customer_id)  
    
        # Check if the customer exists in the database
        customer = Customer.find_by_id(customer_id)
        if not customer:
            raise Unauthorized("Customer not found")
        if expected_id:
            expected_id = ObjectId(expected_id)
            if customer_id != expected_id:
                raise Unauthorized("Access denied: token does not match requested customer")

        return customer_id

    except jwt.ExpiredSignatureError:
        raise Unauthorized("Token has expired")
    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid token")


def get_salesteam_id_from_token(expected_id=None):
    """
    Extracts the JWT token from the Authorization header,
    decodes it using the secret key,
    retrieves the sales team member ID from the payload,
    verifies that the user exists,
    and optionally checks if the token belongs to the expected user.

    Args:
        expected_id (str, optional): ID to compare against the token's user ID.

    Returns:
        dict: The user object if the token is valid and the user exists.

    Raises:
        Unauthorized: If the token is missing, invalid, expired, or does not match the expected user.
    """
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise Unauthorized("Authorization header is missing")

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise Unauthorized("Authorization header must be in 'Bearer <token>' format")

    token = parts[1]
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        salesteam_id = payload.get('salesteam_id')

        if not salesteam_id:
            raise Unauthorized("Token payload is missing 'salesteam_id'")
        
        salesteam_id = ObjectId(salesteam_id)  
    
        # Check if the sales team member exists in the database
        from models.salesteam_model import SalesTeam
        salesteam_member = SalesTeam.find_by_id(salesteam_id)
        if not salesteam_member:
            raise Unauthorized("Sales team member not found")
        if expected_id:
            expected_id = ObjectId(expected_id)
            if salesteam_id != expected_id:
                raise Unauthorized("Access denied: token does not match requested sales team member")

        return salesteam_id

    except jwt.ExpiredSignatureError:
        raise Unauthorized("Token has expired")
    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid token")