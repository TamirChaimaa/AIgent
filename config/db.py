# config/db.py
import os
from pymongo import MongoClient
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
print("✅ Fichier .env chargé avec succès")

# Load environment variables
MONGODB_URI = os.getenv('MONGODB_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'Ecommerce')  # Default database name

print("=== DEBUG: Variables d'environnement MongoDB ===")
print(f"MONGODB_URI: {MONGODB_URI[:30] if MONGODB_URI else 'None'}...")
print(f"MONGODB_URI trouvée: {'✅ Oui' if MONGODB_URI else '❌ Non'}")

if not MONGODB_URI:
    raise Exception("MONGODB_URI not found in environment variables")

try:
    # Create MongoDB client
    client = MongoClient(MONGODB_URI)
    
    # Test the connection
    client.admin.command('ping')
    print("✅ MongoDB connection successful")
    
    # Get the database (specify name explicitly)
    db = client[DATABASE_NAME]
    
    print(f"✅ Database '{DATABASE_NAME}' initialized successfully")
    
except ConfigurationError as e:
    print(f"❌ Database connection error: {e}")
    raise Exception(f"Database initialization error: {e}")
except ServerSelectionTimeoutError as e:
    print(f"❌ Database connection timeout: {e}")
    raise Exception(f"Database initialization error: {e}")
except Exception as e:
    print(f"❌ Database connection error: {e}")
    raise Exception(f"Database initialization error: {e}")