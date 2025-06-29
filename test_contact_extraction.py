#!/usr/bin/env python3
"""
Test script for automatic contact information extraction
Demonstrates how the chatbot asks for contact info and extracts it automatically
"""

import sys
import os
import requests
import json
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.contact_extractor import ContactExtractor

def test_contact_extraction():
    """Test the contact extraction service"""
    
    print("📧 Testing Contact Information Extraction")
    print("=" * 60)
    
    # Test various contact information formats
    test_responses = [
        {
            "response": "Je m'appelle Jean Dupont, mon email est jean.dupont@example.com et mon téléphone est +33123456789",
            "expected": "complete"
        },
        {
            "response": "Mon nom est Marie Martin, email: marie.martin@gmail.com",
            "expected": "partial"
        },
        {
            "response": "Téléphone: 0123456789",
            "expected": "partial"
        },
        {
            "response": "Je m'appelle Pierre Durand",
            "expected": "partial"
        },
        {
            "response": "Bonjour, comment allez-vous ?",
            "expected": "none"
        }
    ]
    
    for i, test_case in enumerate(test_responses, 1):
        print(f"\n📝 Test {i}: {test_case['response']}")
        print("-" * 50)
        
        try:
            # Test contact detection
            is_contact = ContactExtractor.is_contact_info_response(test_case['response'])
            print(f"🔍 Contact Detection: {'✅ Yes' if is_contact else '❌ No'}")
            
            # Test extraction
            extracted_data = ContactExtractor.extract_contact_info(test_case['response'])
            print(f"📊 Extracted Data:")
            print(f"   - Name: {extracted_data.get('name', 'None')}")
            print(f"   - Email: {extracted_data.get('email', 'None')}")
            print(f"   - Phone: {extracted_data.get('phone', 'None')}")
            print(f"   - Confidence: {extracted_data.get('confidence', 'None')}")
            print(f"   - Method: {extracted_data.get('extraction_method', 'None')}")
            
            # Test follow-up message
            follow_up = ContactExtractor.generate_follow_up_message(extracted_data)
            print(f"💬 Follow-up: {follow_up}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def test_complete_flow():
    """Test the complete flow: interest detection → contact request → extraction"""
    
    print("\n🔄 Testing Complete Contact Flow")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Step 1: Ask a high-interest question
    print("📝 Step 1: Asking high-interest question")
    high_interest_question = {
        "question": "Je veux acheter un ordinateur portable pour le travail, pouvez-vous me recommander quelque chose ?"
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
            print(f"   - Should Capture Lead: {data.get('should_capture_lead', False)}")
            
            if data.get('should_capture_lead'):
                lead_id = data.get('preliminary_lead_id')
                lead_message = data.get('lead_capture_message', '')
                print(f"   - Lead ID: {lead_id}")
                print(f"   - Lead Message: {lead_message[:150]}...")
                
                # Step 2: Provide contact information
                print(f"\n👤 Step 2: Providing contact information")
                contact_response = {
                    "question": "Je m'appelle Jean Dupont, mon email est jean.dupont@example.com et mon téléphone est +33123456789",
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
                    print(f"   - Follow-up: {contact_data.get('follow_up_message', '')}")
                    
                    # Show extracted contact info
                    extraction = contact_data.get('contact_extraction', {})
                    print(f"   - Extracted Name: {extraction.get('name', 'None')}")
                    print(f"   - Extracted Email: {extraction.get('email', 'None')}")
                    print(f"   - Extracted Phone: {extraction.get('phone', 'None')}")
                    print(f"   - Confidence: {extraction.get('confidence', 'None')}")
                    
                    # Step 3: Verify lead in database
                    print(f"\n📊 Step 3: Verifying lead in database")
                    leads_response = requests.get(f"{base_url}/leads/{lead_id}/messages")
                    
                    if leads_response.status_code == 200:
                        lead_data = leads_response.json()
                        lead_info = lead_data['data']
                        print(f"✅ Lead verified in database")
                        print(f"   - Name: {lead_info.get('name')}")
                        print(f"   - Email: {lead_info.get('email')}")
                        print(f"   - Phone: {lead_info.get('phone')}")
                        print(f"   - Status: {lead_info.get('status')}")
                        print(f"   - Total Messages: {lead_info.get('total_messages', 0)}")
                    else:
                        print(f"❌ Failed to verify lead: {leads_response.text}")
                else:
                    print(f"❌ Failed to process contact info: {contact_response_api.text}")
            else:
                print(f"⚠️  No lead capture triggered (interest too low)")
        else:
            print(f"❌ Failed to get AI response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_partial_contact_info():
    """Test handling of partial contact information"""
    
    print("\n📋 Testing Partial Contact Information")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Create a lead first
    print("👤 Creating a test lead")
    try:
        lead_data = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "+33123456789",
            "interested_products": ["Laptop Pro"]
        }
        
        response = requests.post(
            f"{base_url}/leads",
            json=lead_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            lead_id = response.json()['data']['id']
            print(f"✅ Lead created: {lead_id}")
            
            # Test partial contact info
            print(f"\n📝 Testing partial contact information")
            partial_contact = {
                "question": "Je m'appelle Marie Martin",
                "lead_id": lead_id
            }
            
            partial_response = requests.post(
                f"{base_url}/ai/ask",
                json=partial_contact,
                headers={"Content-Type": "application/json"}
            )
            
            if partial_response.status_code == 200:
                data = partial_response.json()
                print(f"✅ Partial contact processed")
                print(f"   - Answer: {data.get('answer', '')[:100]}...")
                print(f"   - Follow-up: {data.get('follow_up_message', '')}")
                
                extraction = data.get('contact_extraction', {})
                print(f"   - Extracted Name: {extraction.get('name', 'None')}")
                print(f"   - Extracted Email: {extraction.get('email', 'None')}")
                print(f"   - Confidence: {extraction.get('confidence', 'None')}")
            else:
                print(f"❌ Failed to process partial contact: {partial_response.text}")
        else:
            print(f"❌ Failed to create lead: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Main test function"""
    print("🎯 Automatic Contact Information Extraction Test")
    print("=" * 60)
    
    try:
        # Test contact extraction service
        test_contact_extraction()
        
        # Test complete flow
        test_complete_flow()
        
        # Test partial contact info
        test_partial_contact_info()
        
        print("\n✅ All tests completed!")
        print("\n📋 System Features Demonstrated:")
        print("   - Automatic interest detection")
        print("   - Intelligent contact information requests")
        print("   - AI-powered contact information extraction")
        print("   - Regex fallback for reliable extraction")
        print("   - Automatic lead updates with contact info")
        print("   - Smart follow-up messages for missing info")
        print("   - Complete conversation tracking")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 