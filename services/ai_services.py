from services.chat_client import ChatClient
from services.product_context import ProductContextProvider
import json
import re

class AiService:
    def __init__(self):
        # Create a Gemini chat client instance
        self.chat_client = ChatClient()
    
    def ask_question(self, user_message: str) -> dict:
        # Fetch ALL products context with additional contexts
        context = ProductContextProvider.fetch_product_context()
        
        # Start a new chat session with full context
        self.chat_client.start_chat(context)
        
        # Create a comprehensive prompt that uses all contexts
        enhanced_prompt = f"""
        User question: {user_message}
        
        IMPORTANT: Use all available context to provide the best recommendations:
        
        1. PRODUCT FILTERING:
        - Filter products based on the user's specific question (price, features, category)
        - Only recommend products that match the user's requirements
        
        2. PROMOTIONAL OPPORTUNITIES:
        - Mention relevant promotions when applicable
        - Suggest deals that could benefit the user
        
        3. SEASONAL RECOMMENDATIONS:
        - Consider current season for recommendations
        - Suggest seasonal products when relevant
        
        4. CUSTOMER PREFERENCES:
        - Consider budget-friendly options if user seems price-conscious
        - Suggest quality products for users who prioritize quality
        - Recommend convenient and time-saving products
        - Consider eco-friendly options when appropriate
        
        5. CATEGORY INSIGHTS:
        - Use category-specific knowledge for better recommendations
        - Consider what's popular and well-reviewed in each category
        
        Answer the question helpfully, then recommend ONLY the most relevant products.
        Mention any applicable promotions or seasonal considerations.
        
        Format your response EXACTLY like this:
        MESSAGE: [your response message here]
        PRODUCTS: [list of product names separated by commas]
        
        Example:
        MESSAGE: Here are some great kitchen products for you. Don't forget we have 20% off on kitchen appliances this holiday season!
        PRODUCTS: Chef Knife, Cutting Board, Non-stick Pan
        """
        
        # Send the enhanced prompt to Gemini
        response_text = self.chat_client.send_message(enhanced_prompt)
        
        # Parse the response to extract message and products
        return self._parse_ai_response(response_text)
    
    def _parse_ai_response(self, response_text: str) -> dict:
        """Parse the AI response to extract message and product recommendations"""
        try:
            # Extract message part
            message_match = re.search(r'MESSAGE:\s*(.*?)(?=PRODUCTS:|$)', response_text, re.DOTALL)
            message = message_match.group(1).strip() if message_match else response_text
            
            # Extract products part
            products_match = re.search(r'PRODUCTS:\s*(.*)', response_text, re.DOTALL)
            products_text = products_match.group(1).strip() if products_match else ""
            
            # Convert products text to array and get full product details
            recommended_products = []
            if products_text:
                product_names = [name.strip() for name in products_text.split(',')]
                recommended_products = ProductContextProvider.get_products_by_names(product_names)
            
            return {
                'message': message,
                'products': recommended_products
            }
            
        except Exception as e:
            # If parsing fails, return the original response with empty products
            return {
                'message': response_text,
                'products': []
            }