# app.py
from flask import Flask, jsonify
from flasgger import Swagger
from config.db import db 

app = Flask(__name__)
swagger = Swagger(app)

# --- Route GET '/' avec Swagger ---
@app.route('/', methods=['GET'])
def home():
    """
    Accueil de l'API
    ---
    tags:
      - Accueil
    responses:
      200:
        description: Message de bienvenue
        examples:
          application/json: {"message": "Bienvenue dans mon API Flask avec Swagger"}
    """
    return jsonify({"message": "Bienvenue dans mon API Flask avec Swagger"})

if __name__ == '__main__':
    app.run(debug=True)

