#!/usr/bin/env python3
"""
Test script for lead-message linking functionality
Demonstrates how leads are linked with messages and conversation history
"""

import sys
import os
import requests
import json
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_lead_message_linking():
    """Test the complete lead-message linking flow"""
    
    print("🔗 Testing Lead-Message Linking System")
    print("=" * 60)
    
    # Base URL for the Flask API
    base_url = "http://localhost:5000"
    
    # Test scenario: User asks questions, becomes lead, continues conversation
    test_scenario = [
        {
            "question": "Je veux acheter un ordinateur portable pour le travail",
            "expected_interest": "high",
            "step": "Initial high-interest question"
        },
        {
            "question": "Quel est le prix de vos laptops ?",
            "expected_interest": "high", 
            "step": "Follow-up price question"
        },
        {
            "question": "Pouvez-vous me montrer les caractéristiques ?",
            "expected_interest": "medium",
            "step": "Product details question"
        }
    ]
    
    lead_id = None
    message_ids = []
    
    for i, test_case in enumerate(test_scenario, 1):
        print(f"\n📝 Test {i}: {test_case['step']}")
        print(f"Question: {test_case['question']}")
        print("-" * 50)
        
        try:
            # Prepare request data
            request_data = {"question": test_case['question']}
            
            # If we have a lead_id, link to it
            if lead_id:
                request_data['lead_id'] = lead_id
                print(f"🔗 Linking to existing lead: {lead_id}")
            
            # Step 1: Ask AI question
            print("🤖 Asking AI question...")
            ai_response = requests.post(
                f"{base_url}/ai/ask",
                json=request_data,
                headers={"Content-Type": "application/json"}
            )
            
            if ai_response.status_code == 200:
                ai_data = ai_response.json()
                message_id = ai_data.get('message_id')
                message_ids.append(message_id)
                
                print(f"✅ AI Response received")
                print(f"   - Message ID: {message_id}")
                print(f"   - Answer: {ai_data.get('answer', '')[:80]}...")
                
                # Check if lead was created or linked
                if ai_data.get('preliminary_lead_id'):
                    lead_id = ai_data['preliminary_lead_id']
                    print(f"   - 🆕 New lead created: {lead_id}")
                elif ai_data.get('linked_lead_id'):
                    lead_id = ai_data['linked_lead_id']
                    print(f"   - 🔗 Message linked to lead: {lead_id}")
                
                # Check interest analysis
                interest_analysis = ai_data.get('interest_analysis', {})
                print(f"   - Interest Level: {interest_analysis.get('interest_level', 'unknown')}")
                print(f"   - Interest Score: {interest_analysis.get('interest_score', 0)}")
                
            else:
                print(f"❌ AI request failed: {ai_response.status_code} - {ai_response.text}")
                continue
                
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            continue
        
        # Small delay between requests
        time.sleep(1)
    
    # Now test the lead-message linking functionality
    if lead_id:
        print(f"\n🔍 Testing Lead-Message Linking for Lead: {lead_id}")
        print("=" * 60)
        
        # Test 1: Get lead with messages
        print("\n📋 Test 1: Get lead with related messages")
        try:
            response = requests.get(f"{base_url}/leads/{lead_id}/messages")
            if response.status_code == 200:
                data = response.json()
                lead_with_messages = data['data']
                print(f"✅ Lead with messages retrieved")
                print(f"   - Lead Name: {lead_with_messages.get('name')}")
                print(f"   - Lead Email: {lead_with_messages.get('email')}")
                print(f"   - Total Messages: {lead_with_messages.get('total_messages', 0)}")
                print(f"   - Source Message: {lead_with_messages.get('source_message', {}).get('question', 'N/A')[:50]}...")
            else:
                print(f"❌ Failed to get lead with messages: {response.text}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Test 2: Get conversation history
        print("\n💬 Test 2: Get complete conversation history")
        try:
            response = requests.get(f"{base_url}/leads/{lead_id}/conversation")
            if response.status_code == 200:
                data = response.json()
                conversation = data['data']
                print(f"✅ Conversation history retrieved")
                print(f"   - Total Messages: {conversation.get('total_messages', 0)}")
                print(f"   - Conversation Start: {conversation.get('conversation_start')}")
                print(f"   - Conversation End: {conversation.get('conversation_end')}")
                
                # Show first few messages
                messages = conversation.get('messages', [])
                for i, msg in enumerate(messages[:3]):
                    print(f"   - Message {i+1}: {msg.get('question', '')[:50]}...")
            else:
                print(f"❌ Failed to get conversation history: {response.text}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Test 3: Get lead analytics
        print("\n📊 Test 3: Get lead analytics")
        try:
            response = requests.get(f"{base_url}/leads/{lead_id}/analytics")
            if response.status_code == 200:
                data = response.json()
                analytics = data['data']
                print(f"✅ Lead analytics retrieved")
                print(f"   - Total Messages: {analytics.get('total_messages', 0)}")
                print(f"   - Interested Products: {analytics.get('interested_products_count', 0)}")
                print(f"   - Lead Age (days): {analytics.get('lead_age_days', 'N/A')}")
                print(f"   - Conversion Probability: {analytics.get('conversion_probability', 'N/A')}")
            else:
                print(f"❌ Failed to get lead analytics: {response.text}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Test 4: Update lead contact information
        print("\n👤 Test 4: Update lead contact information")
        try:
            contact_data = {
                "name": "Jean Dupont",
                "email": "jean.dupont@example.com",
                "phone": "+33123456789"
            }
            
            response = requests.put(
                f"{base_url}/leads/{lead_id}/contact-info",
                json=contact_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Lead contact info updated")
                print(f"   - Name: {data['data']['name']}")
                print(f"   - Email: {data['data']['email']}")
                print(f"   - Phone: {data['data']['phone']}")
                print(f"   - Status: {data['data']['status']}")
            else:
                print(f"❌ Failed to update contact info: {response.text}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Test 5: Continue conversation with existing lead
        print("\n🔄 Test 5: Continue conversation with existing lead")
        try:
            follow_up_question = {
                "question": "Merci pour les informations. Quand puis-je recevoir ma commande ?",
                "lead_id": lead_id
            }
            
            response = requests.post(
                f"{base_url}/ai/ask",
                json=follow_up_question,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Follow-up question processed")
                print(f"   - Message linked to lead: {data.get('linked_lead_id')}")
                print(f"   - Answer: {data.get('answer', '')[:80]}...")
            else:
                print(f"❌ Failed to process follow-up: {response.text}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    else:
        print("\n⚠️  No lead was created during the test")

def test_message_linking_by_email():
    """Test linking messages by email"""
    
    print("\n📧 Testing Message Linking by Email")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test email
    test_email = "test.user@example.com"
    
    # First, create a lead with this email
    print(f"👤 Creating lead with email: {test_email}")
    try:
        lead_data = {
            "name": "Test User",
            "email": test_email,
            "phone": "+33123456789",
            "interested_products": ["Laptop Pro", "Wireless Mouse"]
        }
        
        response = requests.post(
            f"{base_url}/leads",
            json=lead_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            lead_id = data['data']['id']
            print(f"✅ Lead created: {lead_id}")
            
            # Now ask a question with the same email
            print(f"\n🤖 Asking question with email: {test_email}")
            question_data = {
                "question": "J'ai une question sur ma commande précédente",
                "email": test_email
            }
            
            ai_response = requests.post(
                f"{base_url}/ai/ask",
                json=question_data,
                headers={"Content-Type": "application/json"}
            )
            
            if ai_response.status_code == 200:
                ai_data = ai_response.json()
                print(f"✅ Question processed")
                print(f"   - Message linked to lead: {ai_data.get('linked_lead_id')}")
                print(f"   - Answer: {ai_data.get('answer', '')[:80]}...")
                
                # Verify the link
                if ai_data.get('linked_lead_id') == lead_id:
                    print(f"   - ✅ Correctly linked to existing lead")
                else:
                    print(f"   - ❌ Not linked to correct lead")
            else:
                print(f"❌ Failed to process question: {ai_response.text}")
        else:
            print(f"❌ Failed to create lead: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Main test function"""
    print("🎯 Lead-Message Linking System Test")
    print("=" * 60)
    
    try:
        # Test complete lead-message linking flow
        test_lead_message_linking()
        
        # Test linking by email
        test_message_linking_by_email()
        
        print("\n✅ All tests completed!")
        print("\n📋 System Features Demonstrated:")
        print("   - Automatic lead creation from high-interest questions")
        print("   - Linking subsequent messages to existing leads")
        print("   - Linking messages by email address")
        print("   - Retrieving lead with all related messages")
        print("   - Complete conversation history tracking")
        print("   - Lead analytics and insights")
        print("   - Contact information management")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 