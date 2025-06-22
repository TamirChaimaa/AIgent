from datetime import datetime
from bson import ObjectId
from config.db import db

class Message:
    collection = db.messages

    @classmethod
    def add_message(cls, conversation_id, sender, content):
        # Add a message to a conversation
        msg = {
            "conversation_id": ObjectId(conversation_id),
            "sender": sender,   # 'customer' or 'ai' or 'salesteam'
            "content": content,
            "timestamp": datetime.utcnow()
        }
        result = cls.collection.insert_one(msg)
        return str(result.inserted_id)

    @classmethod
    def find_by_conversation(cls, conversation_id):
        # Retrieve all messages for a conversation
        return list(cls.collection.find({"conversation_id": ObjectId(conversation_id)}))

    @classmethod
    def delete(cls, _id):
        # Delete a message by ObjectId
        result = cls.collection.delete_one({"_id": ObjectId(_id)})
        return result.deleted_count > 0
