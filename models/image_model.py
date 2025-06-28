from bson import ObjectId
from datetime import datetime
from config.db import db  # Assure-toi que db est l'instance MongoDB

class Image:
    collection = db.images

    @staticmethod
    def create(product_id, filepath):
        image_doc = {
            "product_id": ObjectId(product_id),
            "filepath": filepath,
            "uploaded_at": datetime.utcnow()
        }
        result = Image.collection.insert_one(image_doc)
        return str(result.inserted_id)

    @staticmethod
    def find_by_product_id(product_id):
        images_cursor = Image.collection.find({"product_id": ObjectId(product_id)})
        images = []
        for img in images_cursor:
            img["_id"] = str(img["_id"])
            img["product_id"] = str(img["product_id"])
            img["uploaded_at"] = img["uploaded_at"].isoformat()
            images.append(img)
        return images

    @staticmethod
    def delete(image_id):
        result = Image.collection.delete_one({"_id": ObjectId(image_id)})
        return result.deleted_count == 1
