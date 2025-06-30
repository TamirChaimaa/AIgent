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
            
            # Save the message to database
            message_id = MessageModel.create_message(
                question=user_question,
                answer=answer_message,
                product_ids=product_ids
            )
            
            # Analyze interest level using both methods
            interest_analysis = InterestAnalyzer.analyze_interest_level(user_question, answer_message, ai_response.get('products', []))
            
            # Additional check using the new serious interest detection
            serious_interest = InterestAnalyzer.detect_serious_interest(user_question)
            
            # Combine both analyses - if either method detects high interest, capture lead
            should_capture_lead = interest_analysis.get('should_capture_lead', False) or serious_interest
            
            # Extract contact information from the user question
            contact_data = ContactExtractor.extract_contact_info(user_question)
            
            # Generate lead capture message if needed
            lead_capture_message = None
            linked_lead_id = existing_lead_id
            
            if should_capture_lead and not linked_lead_id:
                lead_capture_message = InterestAnalyzer.generate_lead_capture_message(interest_analysis)
            
            # Prepare response data
            response_data = {
                'question': user_question,
                'answer': answer_message,
                'message_id': message_id,
                'linked_lead_id': linked_lead_id,
                'interest_analysis': {
                    **interest_analysis,
                    'serious_interest_detected': serious_interest,
                    'combined_should_capture': should_capture_lead
                },
                'products': ai_response.get('products', []),
                'contact_extraction': contact_data
            }
            
            # Debug: Print interest analysis results
            print(f"DEBUG - Interest Analysis:")
            print(f"  should_capture_lead: {should_capture_lead}")
            print(f"  serious_interest: {serious_interest}")
            print(f"  interest_analysis: {interest_analysis}")
            print(f"  linked_lead_id: {linked_lead_id}")
            
            # Create lead if user shows interest and no existing lead
            if should_capture_lead and not linked_lead_id:
                # Generate lead capture message
                lead_capture_message = InterestAnalyzer.generate_lead_capture_message(interest_analysis)
                response_data['lead_capture_message'] = lead_capture_message
                response_data['should_capture_lead'] = True
                
                # Create lead with extracted contact information
                interested_products = [p.get('name', '') for p in ai_response.get('products', [])]
                
                # Use extracted contact data or fallback to placeholders
                lead_name = contact_data.get('name') if contact_data.get('name') else "To be provided"
                lead_email = contact_data.get('email') if contact_data.get('email') else "pending@example.com"
                lead_phone = contact_data.get('phone') if contact_data.get('phone') else "To be provided"
                
                # Debug: Print contact extraction results
                print(f"DEBUG - Contact Extraction Results:")
                print(f"  Original contact_data: {contact_data}")
                print(f"  Using name: {lead_name}")
                print(f"  Using email: {lead_email}")
                print(f"  Using phone: {lead_phone}")
                
                # Create lead with extracted data
                lead_id = LeadModel.create_lead(
                    name=lead_name,
                    email=lead_email,
                    phone=lead_phone,
                    interested_products=interested_products,
                    source_message_id=message_id
                )
                
                print(f"DEBUG - Lead Creation Result: {lead_id}")
                
                if lead_id:
                    response_data['preliminary_lead_id'] = lead_id
                    response_data['lead_status'] = 'new' if contact_data.get('confidence') in ['high', 'medium'] else 'pending_contact_info'
                    response_data['lead_created'] = True
                    
                    # If we have good contact data, link the message to the lead
                    if contact_data.get('confidence') in ['high', 'medium']:
                        LeadModel.link_message_to_lead(lead_id, message_id)
                        response_data['linked_lead_id'] = lead_id
                else:
                    print(f"DEBUG - Lead creation failed!")
                    response_data['lead_created'] = False
            else:
                response_data['should_capture_lead'] = False
                print(f"DEBUG - No lead capture: should_capture_lead={should_capture_lead}, linked_lead_id={linked_lead_id}")

            return jsonify(response_data)                  
        
        except Exception as e:             
            # Catch any unexpected error and return a 500 error response             
           # return jsonify({'message': 'AI response failed', 'error': str(e)}), 500
           return jsonify({'message': 'Oops! Something went wrong. Please try again later.'}), 500   
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



