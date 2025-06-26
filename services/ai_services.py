# Import the Gemini chat client for communicating with the AI
from services.chat_client import ChatClient

# Import the product context provider which builds context from MongoDB
from services.product_context import ProductContextProvider

# Util for extracting the customer ID from JWT token in the request
from utils.auth_utils import get_customer_id_from_token

# MongoDB model for conversation documents
from models.conversation_model import Conversation

# MongoDB model for storing question-answer messages
from models.message_model import Message

# AI service class that coordinates user interaction with the Gemini chat and stores the conversation/messages
class AiService:
    def __init__(self):
        # Get the customer ID from the JWT token in the current HTTP request
        self.customer_id = get_customer_id_from_token()

        # Create a Gemini chat client instance
        self.chat_client = ChatClient()

        # Fetch context (products) to guide the AI conversation
        context = ProductContextProvider.fetch_product_context()

        # Start a new Gemini chat session with the product context
        self.chat_client.start_chat(context)

    # Retrieve an active conversation for the customer or create a new one if none exists
    def _get_or_create_conversation(self):
        conv = Conversation.find_active_by_customer(self.customer_id)
        return conv["_id"] if conv else Conversation.create(self.customer_id)

    # Main method for handling user questions and storing the interaction
    def ask_question(self, user_message: str) -> str:
        # Send the question to Gemini and receive the response
        response_text = self.chat_client.send_message(user_message)

        # Save the interaction (question and answer) in the database
        Message.create(
            conversation_id=self._get_or_create_conversation(),
            question=user_message,
            answer=response_text
        )

        # Return the AI's answer to the frontend
        return response_text
