from flask import request, jsonify
from services.ai_services import AiService
from services.interest_analyzer import InterestAnalyzer
from services.contact_extractor import ContactExtractor
from models.message_model import MessageModel
from models.lead_model import LeadModel

# controllers/ai_controller.py
class AiController:     
    @staticmethod     
    def askchat():         
        try:             
            # Parse JSON body and check if the 'question' field exists             
            data = request.json             
            if not data or 'question' not in data:                 
                return jsonify({'message': 'Missing question field'}), 400                          
            
            user_question = data['question']
            user_email = data.get('email')  # Optional: user can provide email
            existing_lead_id = data.get('lead_id')  # Optional: link to existing lead
            
            # Check if this looks like a contact information response
            is_contact_response = ContactExtractor.is_contact_info_response(user_question)
            
            # If it's a contact response and we have a lead_id, extract and update
            if is_contact_response and existing_lead_id:
                return AiController._handle_contact_info_response(user_question, existing_lead_id)
            
            # Instantiate the AI service to handle the question             
            ai_service = AiService()             
            ai_response = ai_service.ask_question(user_question)                          
            
            # Extract product IDs from the response
            product_ids = []
            if ai_response.get('products'):
                product_ids = [product.get('id') for product in ai_response['products'] if product.get('id')]

            # Create the answer message
            answer_message = ai_response.get('message', 'No response generated')
            
            # Save the question and answer to the messages collection
            message_id = MessageModel.create_message(
                question=user_question,
                answer=answer_message,
                product_ids=product_ids
            )

            # Analyze user interest level
            interest_analysis = InterestAnalyzer.analyze_interest_level(
                question=user_question,
                answer=answer_message,
                products=ai_response.get('products', [])
            )

            # Generate lead capture message if interest is high enough
            lead_capture_message = InterestAnalyzer.generate_lead_capture_message(interest_analysis)

            # Prepare response
            response_data = {
                'question': user_question,
                'answer': answer_message,
                'products': ai_response.get('products', []),
                'message_id': message_id,
                'interest_analysis': interest_analysis
            }

            # Check if we should link to existing lead or create new one
            linked_lead_id = None
            
            if existing_lead_id:
                # Link message to existing lead
                LeadModel.link_message_to_lead(existing_lead_id, message_id)
                linked_lead_id = existing_lead_id
                response_data['linked_lead_id'] = linked_lead_id
                response_data['message'] = 'Message linked to existing lead'
            
            elif user_email:
                # Check if lead exists with this email
                existing_lead = LeadModel.get_lead_by_email(user_email)
                if existing_lead:
                    # Link message to existing lead
                    LeadModel.link_message_to_lead(existing_lead['_id'], message_id)
                    linked_lead_id = existing_lead['_id']
                    response_data['linked_lead_id'] = linked_lead_id
                    response_data['message'] = 'Message linked to existing lead'
            
            # Add lead capture message if user shows interest and no existing lead
            if lead_capture_message and not linked_lead_id:
                response_data['lead_capture_message'] = lead_capture_message
                response_data['should_capture_lead'] = True
                
                # Create a preliminary lead record with basic info
                # This will be updated when user provides contact details
                interested_products = [p.get('name', '') for p in ai_response.get('products', [])]
                
                # Create lead with placeholder info (will be updated via API)
                lead_id = LeadModel.create_lead(
                    name="To be provided",  # Will be updated when user fills form
                    email="pending@example.com",  # Will be updated when user fills form
                    phone="To be provided",  # Will be updated when user fills form
                    interested_products=interested_products,
                    source_message_id=message_id
                )
                
                if lead_id:
                    response_data['preliminary_lead_id'] = lead_id
                    response_data['lead_status'] = 'pending_contact_info'
            else:
                response_data['should_capture_lead'] = False

            return jsonify(response_data)                  
        
        except Exception as e:             
            # Catch any unexpected error and return a 500 error response             
            return jsonify({'message': 'AI response failed', 'error': str(e)}), 500
    
    @staticmethod
    def _handle_contact_info_response(user_response: str, lead_id: str):
        """
        Handle contact information response from user
        """
        try:
            # Extract contact information from user response
            contact_data = ContactExtractor.extract_contact_info(user_response)
            
            # Generate AI response acknowledging the contact info
            ai_service = AiService()
            ai_response = ai_service.ask_question(
                f"User provided contact information: {user_response}. "
                f"Acknowledge receipt and provide next steps."
            )
            
            answer_message = ai_response.get('message', 'Thank you for your contact information!')
            
            # Save the message
            message_id = MessageModel.create_message(
                question=user_response,
                answer=answer_message,
                product_ids=[]
            )
            
            # Link message to lead
            LeadModel.link_message_to_lead(lead_id, message_id)
            
            # Update lead with extracted contact information
            update_success = False
            if contact_data.get('confidence') in ['high', 'medium']:
                # Only update if we have some valid information
                update_data = {}
                if contact_data.get('name') and contact_data['name'] != "To be provided":
                    update_data['name'] = contact_data['name']
                if contact_data.get('email') and contact_data['email'] != "pending@example.com":
                    update_data['email'] = contact_data['email']
                if contact_data.get('phone') and contact_data['phone'] != "To be provided":
                    update_data['phone'] = contact_data['phone']
                
                if update_data:
                    # Update lead status to 'new' if we have contact info
                    update_data['status'] = 'new'
                    
                    # Update the lead
                    from bson import ObjectId
                    from config.db import db
                    from datetime import datetime
                    
                    update_data['last_contact'] = datetime.utcnow().isoformat() + "Z"
                    
                    result = db.leads.update_one(
                        {"_id": ObjectId(lead_id)},
                        {"$set": update_data}
                    )
                    update_success = result.modified_count > 0
            
            # Generate follow-up message if needed
            follow_up_message = ContactExtractor.generate_follow_up_message(contact_data)
            
            # Prepare response
            response_data = {
                'question': user_response,
                'answer': answer_message,
                'message_id': message_id,
                'linked_lead_id': lead_id,
                'contact_extraction': contact_data,
                'lead_updated': update_success,
                'follow_up_message': follow_up_message,
                'message': 'Contact information processed'
            }
            
            return jsonify(response_data)
            
        except Exception as e:
            return jsonify({
                'message': 'Error processing contact information',
                'error': str(e)
            }), 500



