import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging

# Load environment variables from the .env file
load_dotenv()

class ChatClient:
    def __init__(self, model_name="models/gemini-1.5-flash"):
        """
        Initializes the chat client by loading the API key,
        configuring the generative AI client, and setting the model.
        """
        # Get the Gemini API key from environment variables change tehe api key
        self.api_key = "AIzaSyDva6Ur4GCSIxHELW5ttuN47eK2aQKvXkU"
        
        # If the API key is not set, raise an error
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set.")
        
        # Configure the generative AI client with the API key
        genai.configure(api_key=self.api_key)
        
        # Load the specified Gemini model (default: gemini-1.5-flash)
        self.model = genai.GenerativeModel(model_name)
        
        # Placeholder for the active chat session
        self.chat = None
    
    def start_chat(self, initial_context: str):
        """
        Starts a chat session with an initial context.
        This context guides the AI's answers throughout the conversation.
        """
        # Start a new chat with a predefined message history:
        self.chat = self.model.start_chat(history=[
            # User provides the context (e.g., product list)
            {"role": "user", "parts": [initial_context]},
            
            # AI acknowledges and agrees to answer based only on this context
            {"role": "model", "parts": [
                "Okay, I will answer based on this product list and recommend relevant products. I will format my responses with MESSAGE: and PRODUCTS: as requested."
            ]}
        ])
    
    def send_message(self, message: str) -> str:
        """
        Sends a message to the active chat and returns the model's response.
        Raises an error if the chat hasn't been started yet.
        """
        # Ensure that the chat session is initialized
        if not self.chat:
            raise RuntimeError("Chat not started")
        
        try:
            # Send the message to the model and receive the response
            response = self.chat.send_message(message)
            
            # Return only the text portion of the model's reply
            return response.text
        
        except Exception as e:
            # Log any exception that occurs and re-raise it
            logging.error(f"Gemini send_message error: {e}")
            raise