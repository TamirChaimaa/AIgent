
import os
from flask import Flask, jsonify
from flasgger import Swagger
from routes.auth_customer_routes import auth_bp
from routes.auth_salesteam_routes import auth_bp as salesteam_auth_bp
from routes.ai_routes import ai_bp
from routes.product_routes import product_bp  

app = Flask(__name__)

# Flask configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '123456789')

# Attempt to connect to the database on startup
try:
    from config.db import db
    if db is None:
        print("Warning: Database connection failed")
    else:
        print("Database connection successful")
except Exception as e:
    print(f"Database initialization error: {e}")


# Initialize Swagger documentation
swagger = Swagger(app)

# Register customer authentication routes under /auth
app.register_blueprint(auth_bp, url_prefix='/auth')

# Register salesman authentication routes under /salesteam/auth
app.register_blueprint(salesteam_auth_bp, url_prefix='/salesteam/auth')

# Register AI chat routes under /chats
app.register_blueprint(ai_bp, url_prefix='/chats')

# Register product management routes under /products
app.register_blueprint(product_bp, url_prefix='/products')

# Root endpoint for basic API information
@app.route('/')
def home():
    return jsonify({
        "message": "API Ecommerce is running!",
        "endpoints": {
            "auth": "/auth",
            "salesteam_auth": "/salesteam/auth",
            "chats": "/chats",
            "products": "/products",
            "health": "/health"
        }
    })

# Health check endpoint to test database connectivity
@app.route('/health')
def health():
    try:
        from config.db import db, client
        if db is not None:
            # Ping the database to ensure connection
            client.admin.command('ping')
            collections = db.list_collection_names()
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "collections": collections
            })
        else:
            return jsonify({
                "status": "unhealthy",
                "database": "disconnected"
            }), 500
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

# Run the Flask development server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
