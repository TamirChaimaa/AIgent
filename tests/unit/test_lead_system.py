import requests
import json
from datetime import datetime

def test_lead_system():
    """Test the complete lead capture system"""
    
    base_url = "http://localhost:5000"
    
    print("🎯 TESTING LEAD CAPTURE SYSTEM")
    print("=" * 50)
    
    # Test 1: Test AI with high interest question
    print("\n1. 🤖 Testing AI with high interest question:")
    print("-" * 40)
    
    high_interest_questions = [
        "Combien coûte le MacBook Air M2 ? Je veux l'acheter rapidement.",
        "Quel est le prix du Dell XPS 13 ? Je suis très intéressé.",
        "Montrez-moi les meilleurs laptops pour gaming, je veux commander maintenant.",
        "Quelles sont les spécifications du MacBook Pro ? Je voudrais l'acheter."
    ]
    
    for i, question in enumerate(high_interest_questions, 1):
        print(f"\nQuestion {i}: {question}")
        
        ai_data = {"question": question}
        
        try:
            response = requests.post(f"{base_url}/ai/ask", json=ai_data)
            if response.status_code == 200:
                ai_result = response.json()
                
                print(f"✅ AI Response: {ai_result['answer'][:100]}...")
                print(f"📊 Interest Score: {ai_result['interest_analysis']['interest_score']}")
                print(f"🎯 Interest Level: {ai_result['interest_analysis']['interest_level']}")
                print(f"📝 Should Capture Lead: {ai_result['should_capture_lead']}")
                
                if ai_result.get('lead_capture_message'):
                    print(f"💬 Lead Capture Message: {ai_result['lead_capture_message'][:100]}...")
                
                print(f"📦 Products: {len(ai_result.get('products', []))}")
                
            else:
                print(f"❌ AI Error: {response.text}")
        except Exception as e:
            print(f"❌ AI Request failed: {e}")
    
    # Test 2: Test AI with low interest question
    print("\n2. 🤖 Testing AI with low interest question:")
    print("-" * 40)
    
    low_interest_question = "Bonjour, comment allez-vous ?"
    
    try:
        response = requests.post(f"{base_url}/ai/ask", json={"question": low_interest_question})
        if response.status_code == 200:
            ai_result = response.json()
            print(f"✅ Interest Score: {ai_result['interest_analysis']['interest_score']}")
            print(f"🎯 Interest Level: {ai_result['interest_analysis']['interest_level']}")
            print(f"📝 Should Capture Lead: {ai_result['should_capture_lead']}")
        else:
            print(f"❌ AI Error: {response.text}")
    except Exception as e:
        print(f"❌ AI Request failed: {e}")
    
    # Test 3: Create a lead manually
    print("\n3. 👤 Creating a lead manually:")
    print("-" * 40)
    
    lead_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "interested_products": ["MacBook Air M2", "Dell XPS 13"],
        "source_message_id": "68610fb664e52aedfb5c9f95"
    }
    
    try:
        response = requests.post(f"{base_url}/leads", json=lead_data)
        if response.status_code == 201:
            lead_result = response.json()
            print(f"✅ Lead created: {lead_result['data']['id']}")
            print(f"📧 Email: {lead_result['data']['email']}")
            print(f"📦 Interested in: {len(lead_result['data']['interested_products'])} products")
        else:
            print(f"❌ Lead creation error: {response.text}")
    except Exception as e:
        print(f"❌ Lead creation failed: {e}")
    
    # Test 4: Get all leads
    print("\n4. 📋 Getting all leads:")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/leads")
        if response.status_code == 200:
            leads_result = response.json()
            print(f"✅ Total leads: {leads_result.get('count', 0)}")
            for lead in leads_result.get('data', [])[:3]:  # Show first 3
                print(f"   👤 {lead['name']} - {lead['email']} - Status: {lead['status']}")
        else:
            print(f"❌ Get leads error: {response.text}")
    except Exception as e:
        print(f"❌ Get leads failed: {e}")
    
    # Test 5: Get leads by status
    print("\n5. 📊 Getting leads by status:")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/leads/by-status?status=new")
        if response.status_code == 200:
            status_result = response.json()
            print(f"✅ New leads: {status_result.get('count', 0)}")
        else:
            print(f"❌ Status filter error: {response.text}")
    except Exception as e:
        print(f"❌ Status filter failed: {e}")
    
    print("\n✅ LEAD SYSTEM TEST COMPLETED!")

if __name__ == "__main__":
    test_lead_system() 