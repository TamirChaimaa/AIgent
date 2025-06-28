from flask import Blueprint
# Import the AiController class from the controllers module
from controllers.ai_controller import AiController

# Create a Blueprint for AI routes
ai_bp = Blueprint('ai', __name__)

# Route POST /ai/ask
ai_bp.route('/ask/<customer_id>', methods=['POST'])(AiController.ask)
ai_bp.route('/ask', methods=['POST'])(AiController.askchat)

