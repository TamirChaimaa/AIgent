#!/usr/bin/env python3
"""
Test script for serious interest detection and contact extraction
"""

import requests
import json
from services.interest_analyzer import InterestAnalyzer
from services.contact_extractor import ContactExtractor

def test_serious_interest_detection():
    """Test the serious interest detection function"""
    
    print("🎯 Testing Serious Interest Detection")
    print("=" * 50)
    
    # Test cases for serious interest
    test_cases = [
        {
            "message": "Je veux acheter un ordinateur portable",
            "expected": True,
            "description": "Direct purchase intent in French"
        },
        {
            "message": "I want to buy a laptop",
            "expected": True,
            "description": "Direct purchase intent in English"
        },
        {
            "message": "Combien coûte cet ordinateur ?",
            "expected": True,
            "description": "Price inquiry"
        },
        {
            "message": "How much does this cost?",
            "expected": True,
            "description": "Price inquiry in English"
        },
        {
            "message": "C'est parfait pour moi, je vais le prendre",
            "expected": True,
            "description": "Perfect match and purchase intent"
        },
        {
            "message": "This looks good, I'll take it",
            "expected": True,
            "description": "Positive feedback and purchase intent"
        },
        {
            "message": "Quand puis-je le récupérer ?",
            "expected": True,
            "description": "Pickup inquiry"
        },
        {
            "message": "When can I pick it up?",
            "expected": True,
            "description": "Pickup inquiry in English"
        },
        {
            "message": "Bonjour, comment allez-vous ?",
            "expected": False,
            "description": "Just greeting"
        },
        {
            "message": "Hello, how are you?",
            "expected": False,
            "description": "Just greeting in English"
        },
        {
            "message": "Pouvez-vous me donner plus d'informations ?",
            "expected": False,
            "description": "General information request"
        },
        {
            "message": "Can you give me more information?",
            "expected": False,
            "description": "General information request in English"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        result = InterestAnalyzer.detect_serious_interest(test_case["message"])
        status = "✅ PASS" if result == test_case["expected"] else "❌ FAIL"
        
        print(f"\n📝 Test {i}: {test_case['description']}")
        print(f"   Message: {test_case['message']}")
        print(f"   Expected: {test_case['expected']}, Got: {result}")
        print(f"   Status: {status}")

def test_contact_extraction():
    """Test the contact extraction function"""
    
    print("\n\n📞 Testing Contact Information Extraction")
    print("=" * 50)
    
    # Test cases for contact extraction
    test_cases = [
        {
            "message": "Je m'appelle Jean Dupont, mon email est jean.dupont@example.com et mon téléphone est +33123456789",
            "description": "Complete contact info in French"
        },
        {
            "message": "My name is John Smith, email: john.smith@example.com, phone: +1234567890",
            "description": "Complete contact info in English"
        },
        {
            "message": "Je m'appelle Marie Martin, j'ai 25 ans",
            "description": "Name and age in French"
        },
        {
            "message": "My name is Sarah Johnson, I'm 30 years old",
            "description": "Name and age in English"
        },
        {
            "message": "Email: test@example.com, Phone: (555) 123-4567",
            "description": "Email and phone only"
        },
        {
            "message": "Bonjour, comment allez-vous ?",
            "description": "No contact info"
        },
        {
            "message": "Hello, how are you?",
            "description": "No contact info in English"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['description']}")
        print(f"   Message: {test_case['message']}")
        
        try:
            extracted = ContactExtractor.extract_contact_info(test_case["message"])
            print(f"   📊 Extracted Data:")
            print(f"      - Name: {extracted.get('name', 'None')}")
            print(f"      - Email: {extracted.get('email', 'None')}")
            print(f"      - Phone: {extracted.get('phone', 'None')}")
            print(f"      - Age: {extracted.get('age', 'None')}")
            print(f"      - Confidence: {extracted.get('confidence', 'None')}")
            print(f"      - Method: {extracted.get('extraction_method', 'None')}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

def test_complete_flow():
    """Test the complete flow with API calls"""
    
    print("\n\n🔄 Testing Complete Flow with API")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test high interest question
    print("📝 Step 1: Testing high interest question")
    high_interest_question = {
        "question": "Je veux acheter un ordinateur portable pour le travail, combien ça coûte ?"
    }
    
    try:
        response = requests.post(
            f"{base_url}/ai/ask",
            json=high_interest_question,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI Response received")
            print(f"   - Answer: {data.get('answer', '')[:100]}...")
            
            # Check interest analysis
            interest_analysis = data.get('interest_analysis', {})
            print(f"   - Interest Level: {interest_analysis.get('interest_level', 'N/A')}")
            print(f"   - Interest Score: {interest_analysis.get('interest_score', 'N/A')}")
            print(f"   - Serious Interest Detected: {interest_analysis.get('serious_interest_detected', 'N/A')}")
            print(f"   - Should Capture Lead: {data.get('should_capture_lead', False)}")
            
            if data.get('should_capture_lead'):
                lead_id = data.get('preliminary_lead_id')
                lead_message = data.get('lead_capture_message', '')
                print(f"   - Lead ID: {lead_id}")
                print(f"   - Lead Message: {lead_message[:150]}...")
                
                # Test contact info response
                print(f"\n👤 Step 2: Testing contact info response")
                contact_response = {
                    "question": "Je m'appelle Pierre Durand, mon email est pierre.durand@example.com et mon téléphone est +33123456789",
                    "lead_id": lead_id
                }
                
                contact_response_api = requests.post(
                    f"{base_url}/ai/ask",
                    json=contact_response,
                    headers={"Content-Type": "application/json"}
                )
                
                if contact_response_api.status_code == 200:
                    contact_data = contact_response_api.json()
                    print(f"✅ Contact information processed")
                    print(f"   - Answer: {contact_data.get('answer', '')[:100]}...")
                    print(f"   - Lead Updated: {contact_data.get('lead_updated', False)}")
                    
                    # Show extracted contact info
                    extraction = contact_data.get('contact_extraction', {})
                    print(f"   - Extracted Name: {extraction.get('name', 'None')}")
                    print(f"   - Extracted Email: {extraction.get('email', 'None')}")
                    print(f"   - Extracted Phone: {extraction.get('phone', 'None')}")
                    print(f"   - Confidence: {extraction.get('confidence', 'None')}")
                else:
                    print(f"❌ Failed to process contact info: {contact_response_api.text}")
            else:
                print(f"⚠️  No lead capture triggered (interest too low)")
        else:
            print(f"❌ Failed to get AI response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_low_interest_question():
    """Test a low interest question to ensure no lead capture"""
    
    print("\n\n📝 Testing Low Interest Question")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    low_interest_question = {
        "question": "Bonjour, comment allez-vous ?"
    }
    
    try:
        response = requests.post(
            f"{base_url}/ai/ask",
            json=low_interest_question,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI Response received")
            print(f"   - Answer: {data.get('answer', '')[:100]}...")
            
            # Check interest analysis
            interest_analysis = data.get('interest_analysis', {})
            print(f"   - Interest Level: {interest_analysis.get('interest_level', 'N/A')}")
            print(f"   - Interest Score: {interest_analysis.get('interest_score', 'N/A')}")
            print(f"   - Serious Interest Detected: {interest_analysis.get('serious_interest_detected', 'N/A')}")
            print(f"   - Should Capture Lead: {data.get('should_capture_lead', False)}")
            
            if not data.get('should_capture_lead'):
                print(f"✅ Correctly no lead capture for low interest question")
            else:
                print(f"⚠️  Unexpected lead capture for low interest question")
        else:
            print(f"❌ Failed to get AI response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Main test function"""
    print("🎯 Serious Interest Detection and Contact Extraction Test")
    print("=" * 70)
    
    try:
        # Test serious interest detection
        test_serious_interest_detection()
        
        # Test contact extraction
        test_contact_extraction()
        
        # Test complete flow with API
        test_complete_flow()
        
        # Test low interest question
        test_low_interest_question()
        
        print("\n✅ All tests completed!")
        print("\n📋 System Features Demonstrated:")
        print("   - Serious interest detection with keywords and phrases")
        print("   - Contact information extraction with regex patterns")
        print("   - Combined interest analysis (AI + serious interest)")
        print("   - Automatic lead capture for high interest")
        print("   - Contact info processing and lead updates")
        print("   - Proper handling of low interest questions")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 