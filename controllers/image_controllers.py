import os
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
from models.image_model import Image
from utils.helpers import allowed_file
from bson.errors import InvalidId
from bson import ObjectId
from pymongo.errors import PyMongoError

class ImageController:

    @staticmethod
    def upload(product_id):
        """
        Handle image upload for a given product.
        Validates file existence, file type, saves physically and records metadata in DB.
        """
        try:
            # Check if 'image' key is in the uploaded files
            if 'image' not in request.files:
                return jsonify({"error": "Bad Request", "message": "No image file provided"}), 400

            file = request.files['image']

            # Check if a file was selected
            if file.filename == '':
                return jsonify({"error": "Bad Request", "message": "No selected file"}), 400

            # Validate file extension
            if not allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
                return jsonify({"error": "Bad Request", "message": "Invalid file type"}), 400

            # Secure the filename and define the filepath to save
            filename = secure_filename(file.filename)
            filepath = f"/uploads/{filename}"

            # Construct full physical save path
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            # Save the file on disk
            file.save(save_path)

            # Validate product_id format
            try:
                valid_product_id = ObjectId(product_id)
            except InvalidId:
                return jsonify({"error": "Bad Request", "message": "Invalid product ID format"}), 400

            # Create image document in database
            image_id = Image.create(valid_product_id, filepath)

            return jsonify({
                "message": "Image uploaded",
                "image_id": image_id,
                "filepath": filepath
            }), 201

        except PyMongoError as e:
            # Database related error
            return jsonify({"error": "Internal Server Error", "message": "Database error", "details": str(e)}), 500
        except Exception as e:
            # Catch any unexpected errors
            return jsonify({"error": "Internal Server Error", "message": "Unexpected error", "details": str(e)}), 500

    @staticmethod
    def get_images(product_id):
        """
        Retrieve all images related to a specific product.
        """
        try:
            # Validate product_id format
            try:
                valid_product_id = ObjectId(product_id)
            except InvalidId:
                return jsonify({"error": "Bad Request", "message": "Invalid product ID format"}), 400

            images = Image.find_by_product_id(valid_product_id)
            return jsonify(images), 200

        except PyMongoError as e:
            return jsonify({"error": "Internal Server Error", "message": "Database error", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": "Unexpected error", "details": str(e)}), 500

    @staticmethod
    def delete_image(image_id):
        """
        Delete an image by its image_id.
        """
        try:
            # Validate image_id format
            try:
                valid_image_id = ObjectId(image_id)
            except InvalidId:
                return jsonify({"error": "Bad Request", "message": "Invalid image ID format"}), 400

            success = Image.delete(valid_image_id)
            if success:
                return jsonify({"message": "Image deleted"}), 200
            else:
                return jsonify({"error": "Not Found", "message": "Image not found"}), 404

        except PyMongoError as e:
            return jsonify({"error": "Internal Server Error", "message": "Database error", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": "Unexpected error", "details": str(e)}), 500
