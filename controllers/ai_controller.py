from flask import request, jsonify
from services.ai_services import AiService
from models.message_model import MessageModel

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

            # Return both the user's question and the AI's response
            return jsonify({                 
                'question': user_question,                 
                'answer': answer_message,
                'products': ai_response.get('products', []),
                'message_id': message_id
            })                  
        
        except Exception as e:             
            # Catch any unexpected error and return a 500 error response             
            return jsonify({'message': 'AI response failed', 'error': str(e)}), 500



