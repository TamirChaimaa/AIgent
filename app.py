from flask import Flask, jsonify
from flasgger import Swagger
from config.db import db
from routes.auth_customer_routes import auth_bp  
from routes.ai_routes import ai_bp

app = Flask(__name__)
swagger = Swagger(app)

# Register the auth blueprint with prefix '/auth'
app.register_blueprint(auth_bp, url_prefix='/auth')

# Register the AI blueprint with prefix '/chats'
app.register_blueprint(ai_bp, url_prefix='/chats')

if __name__ == '__main__':
    app.run(debug=True)
