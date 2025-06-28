from datetime import datetime
from bson import ObjectId
from config.db import db

class SalesTeam:
    collection = db.salesteam

    @classmethod
    def create(cls, data):
        # Insert a new sales team member document
        data.setdefault("created_at", datetime.utcnow())
        result = cls.collection.insert_one(data)
        return str(result.inserted_id)

    @classmethod
    def find_by_id(cls, _id):
        # Find a sales team member by ObjectId
        return cls.collection.find_one({"_id": ObjectId(_id)})

    @classmethod
    def find_by_email(cls, email):
        # Find a sales team member by email
        return cls.collection.find_one({"email": email})

    @classmethod
    def find_all(cls, filter=None):
        # Retrieve all sales team members matching filter or all
        filter = filter or {}
        return list(cls.collection.find(filter))

    @classmethod
    def update(cls, _id, update_data):
        # Update sales team member document by ObjectId
        update_data["updated_at"] = datetime.utcnow()
        result = cls.collection.update_one(
            {"_id": ObjectId(_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    @classmethod
    def delete(cls, _id):
        # Delete sales team member document by ObjectId
        result = cls.collection.delete_one({"_id": ObjectId(_id)})
        return result.deleted_count > 0
