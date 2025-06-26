from config.db import db  # Import MongoDB connection instance
import logging  # For logging error messages

# Service to build product context from the database for the AI chat
class ProductContextProvider:
    @staticmethod
    def fetch_product_context() -> str:
        try:
            # Fetch all products from the MongoDB 'products' collection
            products = db.products.find()

            # Initialize a context string for the AI
            context = "Here is a list of available products:\n"

            # Iterate over each product and build a readable string
            for p in products:
                name = p.get("name", "Unknown product")
                description = p.get("description", "No description")
                price = p.get("price", "N/A")
                tags = p.get("tags", [])
                usage_str = ", ".join(tags) if tags else "general use"
                context += f"- {name}: {description}. Price: ${price}. Use: {usage_str}\n"

            return context

        # Log and raise error if context fetching fails
        except Exception as e:
            logging.error(f"Error fetching product context: {e}")
            raise RuntimeError("Failed to fetch product context from DB.")
