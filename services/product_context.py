from config.db import db
import logging

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
            
            context += "\nWhen you recommend products, use exactly the names as they appear in this list."
            
            return context
        
        except Exception as e:
            logging.error(f"Error fetching product context: {e}")
            raise RuntimeError("Failed to fetch product context from DB.")
    
    @staticmethod
    def get_products_by_names(product_names: list) -> list:
        """Get full product details by product names"""
        try:
            # Create a case-insensitive regex pattern for each product name
            regex_patterns = [{"name": {"$regex": name, "$options": "i"}} for name in product_names if name]
            
            if not regex_patterns:
                return []
            
            # Find products that match any of the names
            products = db.products.find({"$or": regex_patterns})
            
            # Convert to list and format for JSON response
            product_list = []
            for product in products:
                product_dict = {
                    "id": str(product.get("_id", "")),
                    "name": product.get("name", ""),
                    "description": product.get("description", ""),
                    "price": product.get("price", 0),
                    "tags": product.get("tags", []),
                    "image": product.get("image", ""),
                    # Ajoutez d'autres champs selon votre structure de base de données
                }
                product_list.append(product_dict)
            
            return product_list
            
        except Exception as e:
            logging.error(f"Error getting products by names: {e}")
            return []

