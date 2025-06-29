import os
from flask import Flask, jsonify, send_from_directory
from flasgger import Swagger
from flask_cors import CORS

# Création de l'application Flask
app = Flask(__name__)

# Configuration CORS - Autorise tous les domaines, méthodes et certains headers
CORS(app,
     origins=['*'],  # Autorise TOUS les domaines à accéder à votre API
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],  # Méthodes HTTP autorisées
     allow_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Credentials'],  # Headers autorisés
     supports_credentials=True  # Autorise l'envoi de cookies/credentials
)

# Flask configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '123456789')

# Upload folder configuration
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

# Import blueprints
from routes.ai_routes import ai_bp
from routes.message_routes import message_bp
from routes.lead_routes import lead_bp

# Register blueprints

app.register_blueprint(ai_bp, url_prefix='/ai')
app.register_blueprint(message_bp, url_prefix='/messages')
app.register_blueprint(lead_bp, url_prefix='/leads')

# Root endpoint for basic API information
@app.route('/')
def home():
    return jsonify({
        "message": "API Ecommerce is running!",
        "endpoints": {
            "auth": "/auth",
            "salesteam_auth": "/salesteam/auth",
            "ai": "/ai",
            "products": "/products",
            "images": "/images",
            "messages": "/messages",
            "leads": "/leads",
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

# Route to serve uploaded images
@app.route('/uploads/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Run the Flask development server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
