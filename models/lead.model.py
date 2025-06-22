from datetime import datetime
from bson import ObjectId
from config.db import db

class Lead:
    collection = db.leads

    @classmethod
    def create(cls, customer_id, conversation_id, interested_product_ids):
        # Create a new lead linked to customer, conversation, and products
        lead = {
            "customer_id": ObjectId(customer_id),
            "conversation_id": ObjectId(conversation_id),
            "interested_product_ids": [ObjectId(pid) for pid in interested_product_ids],
            "qualified": False,
            "created_at": datetime.utcnow()
        }
        result = cls.collection.insert_one(lead)
        return str(result.inserted_id)

    @classmethod
    def find_by_id(cls, _id):
        # Find a lead by ObjectId
        return cls.collection.find_one({"_id": ObjectId(_id)})

    @classmethod
    def find_all(cls, filter=None):
        # Retrieve all leads matching filter or all
        filter = filter or {}
        return list(cls.collection.find(filter))

    @classmethod
    def qualify_lead(cls, lead_id):
        # Mark lead as qualified
        result = cls.collection.update_one(
            {"_id": ObjectId(lead_id)},
            {"$set": {"qualified": True}}
        )
        return result.modified_count > 0

    @classmethod
    def delete(cls, _id):
        # Delete a lead document by ObjectId
        result = cls.collection.delete_one({"_id": ObjectId(_id)})
        return result.deleted_count > 0
