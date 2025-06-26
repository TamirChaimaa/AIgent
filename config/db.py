# config/db.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file (pour développement local)
load_dotenv()

# Récupérer l'URI MongoDB directement ou construire à partir des variables
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    # Fallback: construire l'URI à partir des variables individuelles
    username = os.getenv("MONGO_USERNAME")
    password = os.getenv("MONGO_PASSWORD")
    host = os.getenv("MONGO_HOST")
    database_name = os.getenv("MONGO_DATABASE")
    app_name = os.getenv("MONGO_APP_NAME")
    
    if all([username, password, host, database_name]):
        MONGO_URI = (
            f"mongodb+srv://{username}:{password}@{host}/{database_name}"
            f"?retryWrites=true&w=majority&appName={app_name}"
        )
    else:
        raise ValueError("MongoDB configuration variables are missing")

try:
    # --- Connect to MongoDB Atlas ---
    client = MongoClient(MONGO_URI)
    
    # Test de connexion
    client.admin.command('ping')
    
    # Use "Ecommerce" as the default database
    db = client.get_database("Ecommerce")
    
    # List all collections in the database
    collections = db.list_collection_names()
    
    # Print success message and available collections
    print("Successfully connected to MongoDB Atlas")
    print("Available collections:", collections)

except Exception as e:
    # Print error message if the connection fails
    print("Failed to connect to MongoDB Atlas")
    print("Error:", e)
    
    # Set db to None to indicate failure
    db = None