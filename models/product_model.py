from datetime import datetime
from bson import ObjectId
from config.db import db

class Product:
    collection = db.products

    @classmethod
    def create(cls, data):
        # Insert a new product document
        data.setdefault("created_at", datetime.utcnow())
        result = cls.collection.insert_one(data)
        return str(result.inserted_id)

    @classmethod
    def find_by_id(cls, _id):
        # Find a product by ObjectId
        return cls.collection.find_one({"_id": ObjectId(_id)})

    @classmethod
    def find_all(cls, filter=None):
        # Retrieve all products matching filter or all
        filter = filter or {}
        return list(cls.collection.find(filter))

    @classmethod
    def update(cls, _id, update_data):
        # Update a product document by ObjectId
        update_data["updated_at"] = datetime.utcnow()
        result = cls.collection.update_one(
            {"_id": ObjectId(_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    @classmethod
    def delete(cls, _id):
        # Delete a product document by ObjectId
        result = cls.collection.delete_one({"_id": ObjectId(_id)})
        return result.deleted_count > 0
