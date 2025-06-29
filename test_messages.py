import requests
import json
from datetime import datetime

def test_message_system():
    """Test the complete message system"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 TESTING MESSAGE SYSTEM")
    print("=" * 50)
    
    # Test 1: Ask AI a question (this should automatically save to messages)
    print("\n1. 🤖 Testing AI question (auto-save to messages):")
    print("-" * 40)
    
    ai_data = {
        "question": "Show me laptops under $1000"
    }
    
    try:
        response = requests.post(f"{base_url}/ai/ask", json=ai_data)
        if response.status_code == 200:
            ai_result = response.json()
            print(f"✅ AI Response: {ai_result['answer']}")
            print(f"📝 Message ID: {ai_result.get('message_id')}")
            print(f"📦 Products found: {len(ai_result.get('products', []))}")
        else:
            print(f"❌ AI Error: {response.text}")
    except Exception as e:
        print(f"❌ AI Request failed: {e}")
    
    # Test 2: Get all messages
    print("\n2. 📋 Getting all messages:")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/messages")
        if response.status_code == 200:
            messages_result = response.json()
            print(f"✅ Total messages: {messages_result.get('count', 0)}")
            for msg in messages_result.get('data', [])[:3]:  # Show first 3
                print(f"   📝 {msg['question'][:50]}... -> {msg['answer'][:50]}...")
        else:
            print(f"❌ Get messages error: {response.text}")
    except Exception as e:
        print(f"❌ Get messages failed: {e}")
    
    # Test 3: Create a manual message
    print("\n3. ✏️ Creating manual message:")
    print("-" * 40)
    
    manual_data = {
        "question": "What are the best gaming laptops?",
        "answer": "Based on our selection, the ASUS ROG Strix G15 is excellent for gaming with RTX 3060 graphics.",
        "product_ids": ["64f82cd187b5c8e9c2fd1234", "64f82cd187b5c8e9c2fd5678"]
    }
    
    try:
        response = requests.post(f"{base_url}/messages", json=manual_data)
        if response.status_code == 201:
            manual_result = response.json()
            print(f"✅ Manual message created: {manual_result['data']['id']}")
        else:
            print(f"❌ Manual message error: {response.text}")
    except Exception as e:
        print(f"❌ Manual message failed: {e}")
    
    # Test 4: Get messages by date range
    print("\n4. 📅 Getting messages by date range:")
    print("-" * 40)
    
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        response = requests.get(f"{base_url}/messages/date-range?start_date={today}T00:00:00Z&end_date={today}T23:59:59Z")
        if response.status_code == 200:
            date_result = response.json()
            print(f"✅ Messages today: {date_result.get('count', 0)}")
        else:
            print(f"❌ Date range error: {response.text}")
    except Exception as e:
        print(f"❌ Date range failed: {e}")
    
    # Test 5: Get messages by product IDs
    print("\n5. 🏷️ Getting messages by product IDs:")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/messages/by-products?product_ids=64f82cd187b5c8e9c2fd1234,64f82cd187b5c8e9c2fd5678")
        if response.status_code == 200:
            product_result = response.json()
            print(f"✅ Messages for products: {product_result.get('count', 0)}")
        else:
            print(f"❌ Product filter error: {response.text}")
    except Exception as e:
        print(f"❌ Product filter failed: {e}")
    
    print("\n✅ MESSAGE SYSTEM TEST COMPLETED!")

if __name__ == "__main__":
    test_message_system() 