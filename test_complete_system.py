#!/usr/bin/env python3
"""
Test script for the complete AI-powered lead capture system
Demonstrates the full flow: AI question → Interest analysis → Lead creation → Contact info update
"""

import sys
import os
import requests
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_complete_lead_capture_flow():
    """Test the complete lead capture flow"""
    
    print("🚀 Testing Complete Lead Capture System")
    print("=" * 60)
    
    # Base URL for the Flask API
    base_url = "http://localhost:5000"
    
    # Test questions that should trigger lead capture
    test_questions = [
        {
            "question": "Je veux acheter un ordinateur portable pour le travail, pouvez-vous me recommander quelque chose ?",
            "expected_interest": "high"
        },
        {
            "question": "Quel est le prix de vos laptops ? J'ai besoin d'acheter rapidement",
            "expected_interest": "high"
        },
        {
            "question": "Pouvez-vous me montrer vos produits ?",
            "expected_interest": "medium"
        }
    ]
    
    for i, test_case in enumerate(test_questions, 1):
        print(f"\n📝 Test {i}: {test_case['question']}")
        print("-" * 50)
        
        try:
            # Step 1: Ask AI question
            print("🤖 Step 1: Asking AI question...")
            ai_response = requests.post(
                f"{base_url}/ai/ask",
                json={"question": test_case['question']},
                headers={"Content-Type": "application/json"}
            )
            
            if ai_response.status_code == 200:
                ai_data = ai_response.json()
                print(f"✅ AI Response received")
                print(f"   - Answer: {ai_data.get('answer', '')[:100]}...")
                print(f"   - Products: {len(ai_data.get('products', []))} recommended")
                print(f"   - Message ID: {ai_data.get('message_id')}")
                
                # Step 2: Check interest analysis
                interest_analysis = ai_data.get('interest_analysis', {})
                print(f"\n🎯 Step 2: Interest Analysis")
                print(f"   - Interest Score: {interest_analysis.get('interest_score', 0)}")
                print(f"   - Interest Level: {interest_analysis.get('interest_level', 'unknown')}")
                print(f"   - Should Capture Lead: {interest_analysis.get('should_capture_lead', False)}")
                
                # Step 3: Check if lead capture is triggered
                if ai_data.get('should_capture_lead'):
                    print(f"\n📧 Step 3: Lead Capture Triggered")
                    print(f"   - Lead Capture Message: {ai_data.get('lead_capture_message', '')[:100]}...")
                    print(f"   - Preliminary Lead ID: {ai_data.get('preliminary_lead_id')}")
                    print(f"   - Lead Status: {ai_data.get('lead_status')}")
                    
                    # Step 4: Update lead with contact information
                    if ai_data.get('preliminary_lead_id'):
                        print(f"\n👤 Step 4: Updating Lead Contact Info")
                        
                        contact_data = {
                            "name": f"Test User {i}",
                            "email": f"testuser{i}@example.com",
                            "phone": f"+1234567890{i}"
                        }
                        
                        update_response = requests.put(
                            f"{base_url}/leads/{ai_data['preliminary_lead_id']}/contact-info",
                            json=contact_data,
                            headers={"Content-Type": "application/json"}
                        )
                        
                        if update_response.status_code == 200:
                            update_data = update_response.json()
                            print(f"✅ Lead contact info updated successfully")
                            print(f"   - Name: {update_data['data']['name']}")
                            print(f"   - Email: {update_data['data']['email']}")
                            print(f"   - Phone: {update_data['data']['phone']}")
                            print(f"   - Status: {update_data['data']['status']}")
                        else:
                            print(f"❌ Failed to update lead contact info: {update_response.text}")
                    
                    # Step 5: Verify lead in database
                    print(f"\n📊 Step 5: Verifying Lead in Database")
                    leads_response = requests.get(f"{base_url}/leads")
                    
                    if leads_response.status_code == 200:
                        leads_data = leads_response.json()
                        print(f"✅ Found {leads_data['count']} leads in database")
                        
                        # Find our lead
                        our_lead = None
                        for lead in leads_data['data']:
                            if lead.get('_id') == ai_data.get('preliminary_lead_id'):
                                our_lead = lead
                                break
                        
                        if our_lead:
                            print(f"✅ Our lead found in database")
                            print(f"   - Name: {our_lead.get('name')}")
                            print(f"   - Email: {our_lead.get('email')}")
                            print(f"   - Status: {our_lead.get('status')}")
                            print(f"   - Interested Products: {our_lead.get('interested_products', [])}")
                        else:
                            print(f"❌ Our lead not found in database")
                else:
                    print(f"\n⚠️  Step 3: No Lead Capture (Interest too low)")
                
                # Verify expected interest level
                expected = test_case['expected_interest']
                actual = interest_analysis.get('interest_level', 'unknown')
                if actual == expected:
                    print(f"\n✅ Expected Interest Level: {expected} ✓")
                else:
                    print(f"\n❌ Expected: {expected}, Got: {actual}")
                    
            else:
                print(f"❌ AI request failed: {ai_response.status_code} - {ai_response.text}")
                
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
        
        print()

def test_lead_management():
    """Test lead management operations"""
    
    print("\n🔧 Testing Lead Management Operations")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    try:
        # Test getting all leads
        print("📋 Getting all leads...")
        response = requests.get(f"{base_url}/leads")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['count']} leads")
            
            if data['count'] > 0:
                # Test getting leads by status
                print("\n📊 Getting leads by status...")
                status_response = requests.get(f"{base_url}/leads/status?status=new")
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"✅ Found {status_data['count']} leads with status 'new'")
                    
                    # Test updating lead status
                    if status_data['count'] > 0:
                        lead_id = status_data['data'][0]['_id']
                        print(f"\n🔄 Updating lead status...")
                        
                        update_data = {
                            "status": "contacted",
                            "notes": "Test status update"
                        }
                        
                        update_response = requests.put(
                            f"{base_url}/leads/{lead_id}/status",
                            json=update_data,
                            headers={"Content-Type": "application/json"}
                        )
                        
                        if update_response.status_code == 200:
                            print(f"✅ Lead status updated successfully")
                        else:
                            print(f"❌ Failed to update lead status: {update_response.text}")
                else:
                    print(f"❌ Failed to get leads by status: {status_response.text}")
        else:
            print(f"❌ Failed to get leads: {response.text}")
            
    except Exception as e:
        print(f"❌ Lead management test failed: {str(e)}")

def main():
    """Main test function"""
    print("🎯 Complete System Test")
    print("=" * 60)
    
    try:
        # Test complete lead capture flow
        test_complete_lead_capture_flow()
        
        # Test lead management operations
        test_lead_management()
        
        print("\n✅ All tests completed!")
        print("\n📋 System Summary:")
        print("   - AI analyzes user questions for interest")
        print("   - High interest triggers lead capture")
        print("   - Preliminary lead created automatically")
        print("   - User provides contact info via API")
        print("   - Lead status managed through API")
        print("   - All data stored in MongoDB collections")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 