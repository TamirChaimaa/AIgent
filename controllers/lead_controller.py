from flask import request, jsonify
from models.lead_model import LeadModel
from config.db import db
from datetime import datetime
from pymongo import MongoClient

class LeadController:
    @staticmethod
    def create_lead():
        """
        Create a new lead
        """
        try:
            data = request.json
            
            # Validate required fields
            required_fields = ['name', 'email', 'phone']
            for field in required_fields:
                if not data or field not in data:
                    return jsonify({
                        'success': False,
                        'message': f'{field} is required'
                    }), 400
            
            name = data['name']
            email = data['email']
            phone = data['phone']
            interested_products = data.get('interested_products', []) if data else []
            source_message_id = data.get('source_message_id') if data else None
            
            # Check if lead already exists
            existing_lead = LeadModel.get_lead_by_email(email)
            if existing_lead:
                return jsonify({
                    'success': False,
                    'message': 'A lead with this email already exists'
                }), 409
            
            # Create the lead
            lead_id = LeadModel.create_lead(
                name=name,
                email=email,
                phone=phone,
                interested_products=interested_products,
                source_message_id=source_message_id
            )
            
            if lead_id:
                return jsonify({
                    'success': True,
                    'message': 'Lead created successfully',
                    'data': {
                        'id': lead_id,
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'interested_products': interested_products,
                        'status': 'new',
                        'created_at': datetime.utcnow().isoformat() + "Z"
                    }
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'message': 'Failed to create lead'
                }), 500
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error creating lead: {str(e)}'
            }), 500
    
    @staticmethod
    def get_all_leads():
        """
        Get all leads
        """
        try:
            leads = LeadModel.get_all_leads()
            
            return jsonify({
                'success': True,
                'data': leads,
                'count': len(leads)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error getting leads: {str(e)}'
            }), 500
    
    @staticmethod
    def get_leads_by_status():
        """
        Get leads by status
        """
        try:
            status = request.args.get('status')
            
            if not status:
                return jsonify({
                    'success': False,
                    'message': 'Status parameter is required'
                }), 400
            
            leads = LeadModel.get_leads_by_status(status)
            
            return jsonify({
                'success': True,
                'data': leads,
                'count': len(leads),
                'filters': {
                    'status': status
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error getting leads by status: {str(e)}'
            }), 500
    
    @staticmethod
    def update_lead_status(lead_id):
        """
        Update lead status
        """
        try:
            data = request.json
            
            if not data or 'status' not in data:
                return jsonify({
                    'success': False,
                    'message': 'Status is required'
                }), 400
            
            status = data['status']
            notes = data.get('notes', '')
            
            # Validate status
            valid_statuses = ['new', 'contacted', 'converted', 'lost']
            if status not in valid_statuses:
                return jsonify({
                    'success': False,
                    'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
                }), 400
            
            success = LeadModel.update_lead_status(lead_id, status, notes)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Lead status updated successfully'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Lead not found or could not be updated'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error updating lead status: {str(e)}'
            }), 500
    
    @staticmethod
    def delete_lead(lead_id):
        """
        Delete a lead
        """
        try:
            success = LeadModel.delete_lead(lead_id)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Lead deleted successfully'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Lead not found or could not be deleted'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error deleting lead: {str(e)}'
            }), 500
    
    @staticmethod
    def update_lead_contact_info(lead_id):
        """
        Update lead contact information (name, email, phone)
        """
        try:
            data = request.json
            
            # Validate required fields
            required_fields = ['name', 'email', 'phone']
            for field in required_fields:
                if not data or field not in data:
                    return jsonify({
                        'success': False,
                        'message': f'{field} is required'
                    }), 400
            
            name = data['name']
            email = data['email']
            phone = data['phone']
            
            # Check if email is already used by another lead
            existing_lead = LeadModel.get_lead_by_email(email)
            if existing_lead and str(existing_lead['_id']) != lead_id:
                return jsonify({
                    'success': False,
                    'message': 'A lead with this email already exists'
                }), 409
            
            # Update the lead with real contact information
            from bson import ObjectId
            update_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "status": "new",  # Change from pending to new
                "last_contact": datetime.utcnow().isoformat() + "Z"
            }
            
            result = db.leads.update_one(
                {"_id": ObjectId(lead_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return jsonify({
                    'success': True,
                    'message': 'Lead contact information updated successfully',
                    'data': {
                        'id': lead_id,
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'status': 'new'
                    }
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Lead not found or could not be updated'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error updating lead contact info: {str(e)}'
            }), 500
    
    @staticmethod
    def get_lead_with_messages(lead_id):
        """
        Get lead with all related messages
        """
        try:
            lead_with_messages = LeadModel.get_lead_with_messages(lead_id)
            
            if lead_with_messages:
                return jsonify({
                    'success': True,
                    'data': lead_with_messages
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Lead not found'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error getting lead with messages: {str(e)}'
            }), 500
    
    @staticmethod
    def get_conversation_history(lead_id):
        """
        Get complete conversation history for a lead
        """
        try:
            conversation = LeadModel.get_conversation_history(lead_id)
            
            if conversation:
                return jsonify({
                    'success': True,
                    'data': conversation
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Lead not found'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error getting conversation history: {str(e)}'
            }), 500
    
    @staticmethod
    def get_lead_analytics(lead_id):
        """
        Get analytics for a lead
        """
        try:
            analytics = LeadModel.get_lead_analytics(lead_id)
            
            if analytics:
                return jsonify({
                    'success': True,
                    'data': analytics
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Lead not found'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error getting lead analytics: {str(e)}'
            }), 500
    
    @staticmethod
    def link_message_to_lead(lead_id):
        """
        Link a message to a lead
        """
        try:
            data = request.json
            
            if not data or 'message_id' not in data:
                return jsonify({
                    'success': False,
                    'message': 'message_id is required'
                }), 400
            
            message_id = data['message_id']
            
            success = LeadModel.link_message_to_lead(lead_id, message_id)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Message linked to lead successfully'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Lead not found or could not be linked'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error linking message to lead: {str(e)}'
            }), 500 