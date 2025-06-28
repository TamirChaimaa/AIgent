from flask import Blueprint
from controllers.image_controllers import ImageController

image_bp = Blueprint('images', __name__)

# Upload image for a product
image_bp.route('/<string:product_id>/upload', methods=['POST'])(ImageController.upload)

# Get all images of a product
image_bp.route('/product/<string:product_id>', methods=['GET'])(ImageController.get_images)

# Delete an image by its ID
image_bp.route('/<string:image_id>', methods=['DELETE'])(ImageController.delete_image)
