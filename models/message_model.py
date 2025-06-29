from datetime import datetime
from bson import ObjectId
from config.db import db

class MessageModel:
    @staticmethod
    def create_message(question: str, answer: str, product_ids: list = None):
        """
        Create a new message record in the messages collection
        """
        try:
            message_data = {
                "question": question,
                "answer": answer,
                "product_ids": product_ids or [],
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            result = db.messages.insert_one(message_data)
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"Error creating message: {e}")
            return None
    
    @staticmethod
    def get_all_messages():
        """
        Get all messages from the collection
        """
        try:
            messages = list(db.messages.find().sort("timestamp", -1))
            # Convert ObjectId to string for JSON serialization
            for message in messages:
                message["_id"] = str(message["_id"])
            return messages
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []
    
    @staticmethod
    def get_messages_by_date_range(start_date: str, end_date: str):
        """
        Get messages within a date range
        """
        try:
            query = {
                "timestamp": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
            messages = list(db.messages.find(query).sort("timestamp", -1))
            for message in messages:
                message["_id"] = str(message["_id"])
            return messages
        except Exception as e:
            print(f"Error getting messages by date range: {e}")
            return []
    
    @staticmethod
    def get_messages_by_product_ids(product_ids: list):
        """
        Get messages that mention specific products
        """
        try:
            query = {
                "product_ids": {
                    "$in": product_ids
                }
            }
            messages = list(db.messages.find(query).sort("timestamp", -1))
            for message in messages:
                message["_id"] = str(message["_id"])
            return messages
        except Exception as e:
            print(f"Error getting messages by product IDs: {e}")
            return []
    
    @staticmethod
    def delete_message(message_id: str):
        """
        Delete a message by ID
        """
        try:
            result = db.messages.delete_one({"_id": ObjectId(message_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting message: {e}")
            return False
