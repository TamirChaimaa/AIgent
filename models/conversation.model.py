from datetime import datetime
from bson import ObjectId
from config.db import db

class Conversation:
    collection = db.conversations

    @classmethod
    def create(cls, customer_id):
        # Create a new conversation linked to a customer
        conv = {
            "customer_id": ObjectId(customer_id),
            "started_at": datetime.utcnow(),
            "ended_at": None,
            "status": "active"
        }
        result = cls.collection.insert_one(conv)
        return str(result.inserted_id)

    @classmethod
    def find_by_id(cls, _id):
        # Find a conversation by ObjectId
        return cls.collection.find_one({"_id": ObjectId(_id)})

    @classmethod
    def find_all_by_customer(cls, customer_id):
        # Find all conversations for a given customer
        return list(cls.collection.find({"customer_id": ObjectId(customer_id)}))

    @classmethod
    def close_conversation(cls, _id):
        # Mark conversation as closed with end time
        result = cls.collection.update_one(
            {"_id": ObjectId(_id)},
            {"$set": {"ended_at": datetime.utcnow(), "status": "closed"}}
        )
        return result.modified_count > 0

    @classmethod
    def delete(cls, _id):
        # Delete a conversation document by ObjectId
        result = cls.collection.delete_one({"_id": ObjectId(_id)})
        return result.deleted_count > 0
