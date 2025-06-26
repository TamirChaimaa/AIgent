from datetime import datetime
from bson import ObjectId
from config.db import db

class Message:
    collection = db.messages

    @classmethod
    def create(cls, conversation_id, question, answer, timestamp=None):
        doc = {
            "conversation_id": ObjectId(conversation_id),
            "question": question,
            "answer": answer,
            "timestamp": timestamp or datetime.utcnow()
        }
        result = cls.collection.insert_one(doc)
        return result

    @classmethod
    def find_by_id(cls, _id):
        return cls.collection.find_one({"_id": ObjectId(_id)})

    @classmethod
    def find_by_conversation_id(cls, conversation_id):
        return list(cls.collection.find({"conversation_id": ObjectId(conversation_id)}).sort("timestamp", 1))

    @classmethod
    def update(cls, _id, update_data):
        update_data["timestamp"] = datetime.utcnow()
        result = cls.collection.update_one(
            {"_id": ObjectId(_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    @classmethod
    def delete(cls, _id):
        result = cls.collection.delete_one({"_id": ObjectId(_id)})
        return result.deleted_count > 0
