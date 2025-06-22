from datetime import datetime
from bson import ObjectId
from config.db import db

class Interaction:
    collection = db.interactions

    @classmethod
    def log_interaction(cls, customer_id, interaction_type, target_id=None):
        # Log an interaction from a customer with optional target (e.g. product)
        interaction = {
            "customer_id": ObjectId(customer_id),
            "type": interaction_type,   # e.g. "click_product", "view_product"
            "target_id": ObjectId(target_id) if target_id else None,
            "timestamp": datetime.utcnow()
        }
        result = cls.collection.insert_one(interaction)
        return str(result.inserted_id)

    @classmethod
    def find_all(cls, filter=None):
        # Retrieve all interactions matching filter or all
        filter = filter or {}
        return list(cls.collection.find(filter))

    @classmethod
    def delete(cls, _id):
        # Delete an interaction document by ObjectId
        result = cls.collection.delete_one({"_id": ObjectId(_id)})
        return result.deleted_count > 0
