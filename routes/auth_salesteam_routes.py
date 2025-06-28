from flask import Blueprint
from controllers.auth_salesteam_controllers import SalesteamAuthController

# Create a new Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# Register the signup route with POST method
# When a POST request is made to /signup, the signup method of AuthController is called
auth_bp.route('/signup', methods=['POST'])(SalesteamAuthController.register)

# Register the login route with POST method
# When a POST request is made to /login, the login method of AuthController is called
auth_bp.route('/login', methods=['POST'])(SalesteamAuthController.login)
