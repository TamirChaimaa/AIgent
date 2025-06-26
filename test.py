import os
from pymongo import MongoClient
from flask import Flask

# Récupération de l'URI MongoDB
MONGODB_URI = os.getenv('MONGODB_URI')

if not MONGODB_URI:
    raise ValueError("MongoDB configuration variables are missing")

# Initialisation du client MongoDB
try:
    client = MongoClient(MONGODB_URI)
    # Test de connexion
    client.admin.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print(f"Database connection error: {e}")
    raise

# Récupération de la base de données (le nom sera extrait de l'URI)
db = client.get_default_database()

def init_db(app: Flask):
    """Initialise la base de données avec l'application Flask"""
    app.config['MONGODB_URI'] = MONGODB_URI
    return db