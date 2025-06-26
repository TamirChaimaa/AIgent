from datetime import datetime
from bson import ObjectId
from config.db import db

class Customer:
    collection = db.customers

    @classmethod
    def create(cls, data):
      data.setdefault("created_at", datetime.utcnow())
      result = cls.collection.insert_one(data)
      return result 


    @classmethod
    def find_by_email(cls, email):
        # Find a customer by their email address
        return cls.collection.find_one({"email": email})

    @classmethod
    def find_by_id(cls, _id):
        # Find a customer by their ObjectId
        return cls.collection.find_one({"_id": ObjectId(_id)})

    @classmethod
    def find_all(cls, filter=None):
        # Retrieve all customers matching the filter (or all if none)
        filter = filter or {}
        return list(cls.collection.find(filter))

    @classmethod
    def update(cls, _id, update_data):
        # Update a customer document by its ObjectId
        update_data["updated_at"] = datetime.utcnow()
        result = cls.collection.update_one(
            {"_id": ObjectId(_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0  # Returns True if document was updated

    @classmethod
    def delete(cls, _id):
        # Delete a customer document by its ObjectId
        result = cls.collection.delete_one({"_id": ObjectId(_id)})
        return result.deleted_count > 0  # Returns True if document was deleted
