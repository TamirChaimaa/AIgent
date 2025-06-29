from flask import Blueprint
from controllers.message_controller import MessageController

# Create a Blueprint for message routes
message_bp = Blueprint('messages', __name__)

# Route POST /messages - Create a new message
message_bp.route('/', methods=['POST'])(MessageController.create_message)

# Route GET /messages - Get all messages
message_bp.route('/', methods=['GET'])(MessageController.get_all_messages)

# Route GET /messages/date-range - Get messages by date range
message_bp.route('/date-range', methods=['GET'])(MessageController.get_messages_by_date_range)

# Route GET /messages/by-products - Get messages by product IDs
message_bp.route('/by-products', methods=['GET'])(MessageController.get_messages_by_products)

# Route DELETE /messages/<message_id> - Delete a specific message
message_bp.route('/<message_id>', methods=['DELETE'])(MessageController.delete_message) 