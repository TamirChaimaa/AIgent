from flask import Blueprint
from controllers.lead_controller import LeadController

# Create a Blueprint for lead routes
lead_bp = Blueprint('leads', __name__)

# Route POST /leads - Create a new lead
lead_bp.route('/', methods=['POST'])(LeadController.create_lead)

# Route GET /leads - Get all leads
lead_bp.route('/', methods=['GET'])(LeadController.get_all_leads)

# Route GET /leads/status - Get leads by status
lead_bp.route('/status', methods=['GET'])(LeadController.get_leads_by_status)

# Route PUT /leads/<lead_id>/status - Update lead status
lead_bp.route('/<lead_id>/status', methods=['PUT'])(LeadController.update_lead_status)

# Route PUT /leads/<lead_id>/contact-info - Update lead contact information
lead_bp.route('/<lead_id>/contact-info', methods=['PUT'])(LeadController.update_lead_contact_info)

# Route DELETE /leads/<lead_id> - Delete a specific lead
lead_bp.route('/<lead_id>', methods=['DELETE'])(LeadController.delete_lead)

# Route GET /leads/<lead_id>/messages - Get lead with related messages
lead_bp.route('/<lead_id>/messages', methods=['GET'])(LeadController.get_lead_with_messages)

# Route GET /leads/<lead_id>/conversation - Get complete conversation history
lead_bp.route('/<lead_id>/conversation', methods=['GET'])(LeadController.get_conversation_history)

# Route GET /leads/<lead_id>/analytics - Get lead analytics
lead_bp.route('/<lead_id>/analytics', methods=['GET'])(LeadController.get_lead_analytics)

# Route POST /leads/<lead_id>/link-message - Link a message to a lead
lead_bp.route('/<lead_id>/link-message', methods=['POST'])(LeadController.link_message_to_lead) 