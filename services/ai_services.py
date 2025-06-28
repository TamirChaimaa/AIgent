
# services/ai_service.py
from services.chat_client import ChatClient
from services.product_context import ProductContextProvider

class AiService:
    def __init__(self):
        # Create a Gemini chat client instance
        self.chat_client = ChatClient()
        
        # Fetch context (products) to guide the AI conversation
        context = ProductContextProvider.fetch_product_context()
        
        # Start a new Gemini chat session with the product context
        self.chat_client.start_chat(context)
    
    # Main method for handling user questions - no database saving
    def ask_question(self, user_message: str) -> str:
        # Send the question to Gemini and receive the response
        response_text = self.chat_client.send_message(user_message)
        
        # Return the AI's answer to the frontend (no database save)
        return response_text
