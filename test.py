# test_connection.py
import os
from pymongo import MongoClient
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError

# Load your URI
MONGODB_URI ="mongodb+srv://chaimaa02tamir:yqNPcsrRyMu3VoX5@ecommerce.s5qxlkt.mongodb.net/?retryWrites=true&w=majority&appName=Ecommerce"  # Replace with your actual URI

try:
    print("Testing MongoDB connection...")
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    
    # Test the connection
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
    
    # List databases
    print("Available databases:", client.list_database_names())
    
except ConfigurationError as e:
    print(f"❌ Configuration Error: {e}")
except ServerSelectionTimeoutError as e:
    print(f"❌ Server Selection Timeout: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
finally:
    try:
        client.close()
    except:
        pass