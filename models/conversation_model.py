from datetime import datetime
from bson import ObjectId
from config.db import db

class Conversation:
    collection = db.conversations

    @classmethod
    def create(cls, customer_id):
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
        return cls.collection.find_one({"_id": ObjectId(_id)})

    @classmethod
    def find_all_by_customer(cls, customer_id):
        return list(cls.collection.find({"customer_id": ObjectId(customer_id)}))

    @classmethod
    def close_conversation(cls, _id):
        result = cls.collection.update_one(
            {"_id": ObjectId(_id)},
            {"$set": {"ended_at": datetime.utcnow(), "status": "closed"}}
        )
        return result.modified_count > 0

    @classmethod
    def delete(cls, _id):
        result = cls.collection.delete_one({"_id": ObjectId(_id)})
        return result.deleted_count > 0

    @classmethod
    def find_active_by_customer(cls, customer_id):
        """
        Retourne la conversation active (status='active') d'un client.
        Renvoie None si aucune conversation active n'est trouvée.
        """
        return cls.collection.find_one({
            "customer_id": ObjectId(customer_id),
            "status": "active"
        })
