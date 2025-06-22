from datetime import datetime
from bson import ObjectId
from config.db import db

class FollowUp:
    collection = db.followups

    @classmethod
    def create(cls, lead_id, sales_id, method, message, status="pending"):
        # Create a follow-up entry linked to lead and sales team member
        followup = {
            "lead_id": ObjectId(lead_id),
            "sales_id": ObjectId(sales_id),
            "method": method,          # e.g. "email", "phone", "sms"
            "message": message,
            "date": datetime.utcnow(),
            "status": status           # e.g. "pending", "done"
        }
        result = cls.collection.insert_one(followup)
        return str(result.inserted_id)

    @classmethod
    def find_by_id(cls, _id):
        # Find a follow-up by ObjectId
        return cls.collection.find_one({"_id": ObjectId(_id)})

    @classmethod
    def find_all(cls, filter=None):
        # Retrieve all follow-ups matching filter or all
        filter = filter or {}
        return list(cls.collection.find(filter))

    @classmethod
    def update_status(cls, followup_id, status):
        # Update the status of a follow-up
        result = cls.collection.update_one(
            {"_id": ObjectId(followup_id)},
            {"$set": {"status": status}}
        )
        return result.modified_count > 0

    @classmethod
    def delete(cls, _id):
        # Delete a follow-up document by ObjectId
        result = cls.collection.delete_one({"_id": ObjectId(_id)})
        return result.deleted_count > 0
