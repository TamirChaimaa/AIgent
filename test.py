#!/usr/bin/env python3
# test_direct_uri.py
from pymongo import MongoClient
import sys

def test_direct_connection():
    # Votre URI MongoDB directe
    MONGO_URI = "mongodb+srv://chaimaa02tamir:yqNPcsrRyMu3VoX5@ecommerce.s5qxlkt.mongodb.net/myDatabase?retryWrites=true&w=majority&appName=Ecommerce"
    
    print("=== DIRECT MONGODB URI TEST ===")
    print(f"Testing URI: {MONGO_URI[:50]}...")
    
    try:
        # Connexion avec timeout court pour test rapide
        client = MongoClient(
            MONGO_URI, 
            serverSelectionTimeoutMS=10000,  # 10 secondes
            connectTimeoutMS=10000,
            socketTimeoutMS=10000
        )
        
        print("🔄 Testing server selection...")
        # Forcer la sélection du serveur
        client.server_info()
        print("✅ Server selection successful!")
        
        print("🔄 Testing admin ping...")
        ping_result = client.admin.command('ping')
        print(f"✅ Admin ping: {ping_result}")
        
        # Tester les bases de données disponibles
        print("🔄 Listing databases...")
        dbs = client.list_database_names()
        print(f"✅ Available databases: {dbs}")
        
        # Tester la base Ecommerce
        ecommerce_db = client.Ecommerce
        collections = ecommerce_db.list_collection_names()
        print(f"✅ Collections in Ecommerce DB: {collections}")
        
        # Tester la base myDatabase (celle dans l'URI)
        my_db = client.myDatabase
        my_collections = my_db.list_collection_names()
        print(f"✅ Collections in myDatabase: {my_collections}")
        
        # Test d'écriture
        print("🔄 Testing write operation...")
        test_collection = ecommerce_db.connection_test
        doc = {"test": "write", "status": "success"}
        result = test_collection.insert_one(doc)
        print(f"✅ Write test successful, ID: {result.inserted_id}")
        
        # Test de lecture
        print("🔄 Testing read operation...")
        found_doc = test_collection.find_one({"_id": result.inserted_id})
        print(f"✅ Read test successful: {found_doc}")
        
        # Nettoyage
        test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Cleanup completed")
        
        client.close()
        print("🎉 ALL TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Connection test FAILED!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        
        # Diagnostic supplémentaire
        if "DNS" in str(e):
            print("💡 DNS Error - Check your internet connection")
        elif "authentication" in str(e).lower():
            print("💡 Authentication Error - Check username/password")
        elif "timeout" in str(e).lower():
            print("💡 Timeout Error - Check network/firewall")
        
        return False

if __name__ == "__main__":
    success = test_direct_connection()
    sys.exit(0 if success else 1)