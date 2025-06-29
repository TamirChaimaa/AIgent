from flask import request, jsonify
from models.message_model import MessageModel
from datetime import datetime

class MessageController:
    @staticmethod
    def create_message():
        """
        Create a new message record
        """
        try:
            data = request.json
            
            # Validate required fields
            if not data or 'question' not in data or 'answer' not in data:
                return jsonify({
                    'success': False,
                    'message': 'Question and answer are required'
                }), 400
            
            question = data['question']
            answer = data['answer']
            product_ids = data.get('product_ids', [])
            
            # Create the message
            message_id = MessageModel.create_message(question, answer, product_ids)
            
            if message_id:
                return jsonify({
                    'success': True,
                    'message': 'Message created successfully',
                    'data': {
                        'id': message_id,
                        'question': question,
                        'answer': answer,
                        'product_ids': product_ids,
                        'timestamp': datetime.utcnow().isoformat() + "Z"
                    }
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'message': 'Failed to create message'
                }), 500
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error creating message: {str(e)}'
            }), 500
    
    @staticmethod
    def get_all_messages():
        """
        Get all messages
        """
        try:
            messages = MessageModel.get_all_messages()
            
            return jsonify({
                'success': True,
                'data': messages,
                'count': len(messages)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error getting messages: {str(e)}'
            }), 500
    
    @staticmethod
    def get_messages_by_date_range():
        """
        Get messages within a date range
        """
        try:
            data = request.args
            
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            
            if not start_date or not end_date:
                return jsonify({
                    'success': False,
                    'message': 'Start date and end date are required'
                }), 400
            
            messages = MessageModel.get_messages_by_date_range(start_date, end_date)
            
            return jsonify({
                'success': True,
                'data': messages,
                'count': len(messages),
                'filters': {
                    'start_date': start_date,
                    'end_date': end_date
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error getting messages by date range: {str(e)}'
            }), 500
    
    @staticmethod
    def get_messages_by_products():
        """
        Get messages that mention specific products
        """
        try:
            data = request.args
            
            product_ids = data.get('product_ids')
            if not product_ids:
                return jsonify({
                    'success': False,
                    'message': 'Product IDs are required'
                }), 400
            
            # Convert comma-separated string to list
            if isinstance(product_ids, str):
                product_ids = product_ids.split(',')
            
            messages = MessageModel.get_messages_by_product_ids(product_ids)
            
            return jsonify({
                'success': True,
                'data': messages,
                'count': len(messages),
                'filters': {
                    'product_ids': product_ids
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error getting messages by products: {str(e)}'
            }), 500
    
    @staticmethod
    def delete_message(message_id):
        """
        Delete a message by ID
        """
        try:
            if not message_id:
                return jsonify({
                    'success': False,
                    'message': 'Message ID is required'
                }), 400
            
            success = MessageModel.delete_message(message_id)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Message deleted successfully'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Message not found or could not be deleted'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error deleting message: {str(e)}'
            }), 500 