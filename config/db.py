# config/db.py
import os
from pymongo import MongoClient
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError

# Try to load environment variables from .env file (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Fichier .env chargé avec succès")
except ImportError:
    print("⚠️ python-dotenv not installed, using system environment variables")
except Exception as e:
    print(f"⚠️ Could not load .env file: {e}")

# Load environment variables
MONGODB_URI = os.getenv('MONGODB_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'Ecommerce')  # Default database name

print("=== DEBUG: Variables d'environnement MongoDB ===")
print(f"MONGODB_URI: {MONGODB_URI[:30] if MONGODB_URI else 'None'}...")
print(f"MONGODB_URI trouvée: {'✅ Oui' if MONGODB_URI else '❌ Non'}")
print(f"DATABASE_NAME: {DATABASE_NAME}")

# List all environment variables for debugging (remove in production)
print("=== DEBUG: All Environment Variables ===")
for key, value in os.environ.items():
    if 'MONGO' in key.upper() or 'DATABASE' in key.upper():
        print(f"{key}: {value[:30]}..." if len(str(value)) > 30 else f"{key}: {value}")

if not MONGODB_URI:
    # Try common alternative environment variable names
    MONGODB_URI = os.getenv('MONGO_URI') or os.getenv('MONGO_URL') or os.getenv('DATABASE_URL')
    
    if not MONGODB_URI:
        raise Exception("MONGODB_URI not found in environment variables. Please set MONGODB_URI, MONGO_URI, or DATABASE_URL")

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