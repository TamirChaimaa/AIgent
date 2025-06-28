from flask import Blueprint
from controllers.product_controllers import ProductController

# Create a new Blueprint for product routes
product_bp = Blueprint('products', __name__)

# Register product routes
product_bp.route('/', methods=['POST'])(ProductController.create)            # Create a new product
product_bp.route('/', methods=['GET'])(ProductController.get_all)            # Get all products
product_bp.route('/<string:product_id>', methods=['GET'])(ProductController.get_by_id)  # Get product by ID
product_bp.route('/<string:product_id>', methods=['PUT'])(ProductController.update)     # Update product
product_bp.route('/<string:product_id>', methods=['DELETE'])(ProductController.delete)  # Delete product
