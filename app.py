import os
from flask import Flask, jsonify
from flasgger import Swagger
from config.db import db
from routes.auth_customer_routes import auth_bp  
from routes.ai_routes import ai_bp

app = Flask(__name__)
swagger = Swagger(app)

# Register the auth blueprint with prefix '/auth'
app.register_blueprint(auth_bp, url_prefix='/auth')

# Register the AI blueprint with prefix test '/chats'
app.register_blueprint(ai_bp, url_prefix='/chats')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
