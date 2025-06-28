from flask import request, jsonify
from bson import ObjectId
from models.product_model import Product
from pymongo.errors import PyMongoError, DuplicateKeyError
from werkzeug.exceptions import BadRequest

class ProductController:

    @staticmethod
    def create():
        """
        Create a new product document in the database.
        Returns:
            - 201 Created: if product is successfully created.
            - 400 Bad Request: if input JSON is missing.
            - 409 Conflict: if a duplicate key error occurs.
            - 500 Internal Server Error: for any other error.
        """
        try:
            data = request.json
            if not data:
                raise BadRequest("Missing JSON data")

            product_id = Product.create(data)
            return jsonify({"message": "Product created", "product_id": product_id}), 201

        except DuplicateKeyError:
            return jsonify({
                "error": "Conflict",
                "message": "Product with the same key already exists"
            }), 409

        except PyMongoError as e:
            return jsonify({
                "error": "Internal Server Error",
                "message": "Database error",
                "details": str(e)
            }), 500

        except BadRequest as e:
            return jsonify({
                "error": "Bad Request",
                "message": str(e)
            }), 400

        except Exception as e:
            return jsonify({
                "error": "Internal Server Error",
                "message": "Unexpected error",
                "details": str(e)
            }), 500

    @staticmethod
    def get_all():
        """
        Retrieve all products from the database.
        Returns:
            - 200 OK: with a list of all products.
            - 500 Internal Server Error: if a database or unknown error occurs.
        """
        try:
            products = Product.find_all()
            for p in products:
                p["_id"] = str(p["_id"])
                p["created_at"] = str(p.get("created_at", ""))
            return jsonify(products), 200

        except PyMongoError as e:
            return jsonify({
                "error": "Internal Server Error",
                "message": "Database error",
                "details": str(e)
            }), 500

        except Exception as e:
            return jsonify({
                "error": "Internal Server Error",
                "message": "Unexpected error",
                "details": str(e)
            }), 500

    @staticmethod
    def get_by_id(product_id):
        """
        Retrieve a product by its ID.
        Args:
            product_id (str): MongoDB ObjectId string
        Returns:
            - 200 OK: with the product if found.
            - 400 Bad Request: if ID format is invalid.
            - 404 Not Found: if product does not exist.
            - 500 Internal Server Error: on other errors.
        """
        try:
            if not ObjectId.is_valid(product_id):
                raise BadRequest("Invalid product ID format")

            product = Product.find_by_id(product_id)
            if product:
                product["_id"] = str(product["_id"])
                product["created_at"] = str(product.get("created_at", ""))
                return jsonify(product), 200

            return jsonify({
                "error": "Not Found",
                "message": "Product not found"
            }), 404

        except BadRequest as e:
            return jsonify({
                "error": "Bad Request",
                "message": str(e)
            }), 400

        except PyMongoError as e:
            return jsonify({
                "error": "Internal Server Error",
                "message": "Database error",
                "details": str(e)
            }), 500

        except Exception as e:
            return jsonify({
                "error": "Internal Server Error",
                "message": "Unexpected error",
                "details": str(e)
            }), 500

    @staticmethod
    def update(product_id):
        """
        Update an existing product by ID.
        Args:
            product_id (str): MongoDB ObjectId string
        Returns:
            - 200 OK: if update successful.
            - 400 Bad Request: if ID or update data is invalid.
            - 404 Not Found: if product does not exist or was not updated.
            - 500 Internal Server Error: on database or unknown error.
        """
        try:
            if not ObjectId.is_valid(product_id):
                raise BadRequest("Invalid product ID format")

            update_data = request.json
            if not update_data:
                raise BadRequest("Missing JSON data for update")

            success = Product.update(product_id, update_data)
            if success:
                return jsonify({"message": "Product updated"}), 200

            return jsonify({
                "error": "Not Found",
                "message": "Product not found or not modified"
            }), 404

        except BadRequest as e:
            return jsonify({
                "error": "Bad Request",
                "message": str(e)
            }), 400

        except PyMongoError as e:
            return jsonify({
                "error": "Internal Server Error",
                "message": "Database error",
                "details": str(e)
            }), 500

        except Exception as e:
            return jsonify({
                "error": "Internal Server Error",
                "message": "Unexpected error",
                "details": str(e)
            }), 500

    @staticmethod
    def delete(product_id):
        """
        Delete a product by ID.
        Args:
            product_id (str): MongoDB ObjectId string
        Returns:
            - 200 OK: if deletion successful.
            - 400 Bad Request: if ID format is invalid.
            - 404 Not Found: if product not found.
            - 500 Internal Server Error: on other errors.
        """
        try:
            if not ObjectId.is_valid(product_id):
                raise BadRequest("Invalid product ID format")

            success = Product.delete(product_id)
            if success:
                return jsonify({"message": "Product deleted"}), 200

            return jsonify({
                "error": "Not Found",
                "message": "Product not found"
            }), 404

        except BadRequest as e:
            return jsonify({
                "error": "Bad Request",
                "message": str(e)
            }), 400

        except PyMongoError as e:
            return jsonify({
                "error": "Internal Server Error",
                "message": "Database error",
                "details": str(e)
            }), 500

        except Exception as e:
            return jsonify({
                "error": "Internal Server Error",
                "message": "Unexpected error",
                "details": str(e)
            }), 500
