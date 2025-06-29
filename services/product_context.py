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
            
            # Iterate over each product and build a detailed string
            for p in products:
                name = p.get("name", "Unknown product")
                description = p.get("description", "No description")
                price = p.get("price", "N/A")
                tags = p.get("tags", [])
                category = p.get("category", "general")
                image_url = p.get("image_url", "")
                
                # Get specifications and other details
                specs = p.get("specs", {})
                brand = p.get("brand", "")
                warranty = p.get("warranty", "")
                rating = p.get("rating", 0)
                reviews_count = p.get("reviews_count", 0)
                available = p.get("available", True)
                release_date = p.get("release_date", "")
                
                usage_str = ", ".join(tags) if tags else "general use"
                
                # Build detailed product string
                product_str = f"- {name}: {description}. Price: ${price}. Category: {category}. Tags: {usage_str}"
                
                # Add laptop/electronics specific information
                if "laptop" in name.lower() or "computer" in name.lower() or "Laptops" in category:
                    if brand:
                        product_str += f". Brand: {brand}"
                    if specs:
                        if specs.get("processor"):
                            product_str += f". CPU: {specs['processor']}"
                        if specs.get("ram"):
                            product_str += f". RAM: {specs['ram']}"
                        if specs.get("storage"):
                            product_str += f". Storage: {specs['storage']}"
                        if specs.get("screen_size"):
                            product_str += f". Screen: {specs['screen_size']}"
                        if specs.get("battery_life"):
                            product_str += f". Battery: {specs['battery_life']}"
                        if specs.get("weight"):
                            product_str += f". Weight: {specs['weight']}"
                        if specs.get("os"):
                            product_str += f". OS: {specs['os']}"
                        if specs.get("keyboard"):
                            product_str += f". Keyboard: {specs['keyboard']}"
                    if warranty:
                        product_str += f". Warranty: {warranty}"
                    if rating:
                        product_str += f". Rating: {rating}/5 ({reviews_count} reviews)"
                    if release_date:
                        product_str += f". Released: {release_date}"
                    if not available:
                        product_str += ". Status: Out of Stock"
                
                context += product_str + "\n"
            
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
                    "category": product.get("category", ""),
                    "image_url": product.get("image_url", ""),
                    "brand": product.get("brand", ""),
                    "warranty": product.get("warranty", ""),
                    "rating": product.get("rating", 0),
                    "reviews_count": product.get("reviews_count", 0),
                    "available": product.get("available", True),
                    "release_date": product.get("release_date", ""),
                    "specs": product.get("specs", {}),
                    "created_at": product.get("created_at", "")
                }
                product_list.append(product_dict)
            
            return product_list
            
        except Exception as e:
            logging.error(f"Error getting products by names: {e}")
            return []
