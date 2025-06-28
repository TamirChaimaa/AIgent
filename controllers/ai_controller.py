from flask import request, jsonify
from services.ai_services import AiService

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
            
            # Return both the user's question and the AI's response
            return jsonify({
                'question': user_question,
                'answer': ai_response
            })
        
        except Exception as e:
            # Catch any unexpected error and return a 500 error response
            return jsonify({'message': 'AI response failed', 'error': str(e)}), 500
