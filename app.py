# app.py
import os
from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)

# Configuration Flask
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '123456789')

# Test de connexion DB au démarrage
try:
    from config.db import db
    if db is None:
        print("Warning: Database connection failed")
    else:
        print("Database connection successful")
except Exception as e:
    print(f"Database initialization error: {e}")

# Importer les routes après la configuration
from routes.auth_customer_routes import auth_bp   
from routes.ai_routes import ai_bp

swagger = Swagger(app)

# Register the auth blueprint with prefix '/auth'
app.register_blueprint(auth_bp, url_prefix='/auth')

# Register the AI blueprint with prefix '/chats'
app.register_blueprint(ai_bp, url_prefix='/chats')

@app.route('/')
def home():
    return jsonify({
        "message": "API Ecommerce is running!",
        "endpoints": {
            "auth": "/auth",
            "chats": "/chats",
            "health": "/health"
        }
    })

@app.route('/health')
def health():
    try:
        from config.db import db, client
        if db is not None:
            # Test ping
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)