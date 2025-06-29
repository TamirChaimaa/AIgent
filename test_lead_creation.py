#!/usr/bin/env python3
"""
Test script for lead creation with extracted contact information
"""

import requests
import json

def test_lead_creation_with_contact_info():
    """Test creating a lead with contact information in the same message"""
    
    print("🎯 Testing Lead Creation with Contact Information")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test case 1: User provides contact info in the same message as interest
    print("📝 Test 1: Interest + Contact Info in same message")
    test_message = "Je veux acheter un ordinateur portable. Je m'appelle Jean Dupont, mon email est jean.dupont@example.com et mon téléphone est +33123456789"
    
    try:
        response = requests.post(
            f"{base_url}/ai/ask",
            json={"question": test_message},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response received")
            print(f"   - Answer: {data.get('answer', '')[:100]}...")
            print(f"   - Should Capture Lead: {data.get('should_capture_lead', False)}")
            
            # Check contact extraction
            contact_extraction = data.get('contact_extraction', {})
            print(f"   - Contact Extraction:")
            print(f"     * Name: {contact_extraction.get('name', 'None')}")
            print(f"     * Email: {contact_extraction.get('email', 'None')}")
            print(f"     * Phone: {contact_extraction.get('phone', 'None')}")
            print(f"     * Confidence: {contact_extraction.get('confidence', 'None')}")
            
            # Check lead creation
            if data.get('should_capture_lead'):
                lead_id = data.get('preliminary_lead_id')
                lead_status = data.get('lead_status')
                lead_created = data.get('lead_created', False)
                
                print(f"   - Lead Creation:")
                print(f"     * Lead ID: {lead_id}")
                print(f"     * Lead Status: {lead_status}")
                print(f"     * Lead Created: {lead_created}")
                
                # Verify lead in database
                if lead_id:
                    print(f"\n📊 Verifying lead in database...")
                    lead_response = requests.get(f"{base_url}/leads/{lead_id}/messages")
                    
                    if lead_response.status_code == 200:
                        lead_data = lead_response.json()
                        lead_info = lead_data['data']
                        print(f"✅ Lead verified in database:")
                        print(f"   - Name: {lead_info.get('name')}")
                        print(f"   - Email: {lead_info.get('email')}")
                        print(f"   - Phone: {lead_info.get('phone')}")
                        print(f"   - Status: {lead_info.get('status')}")
                    else:
                        print(f"❌ Failed to verify lead: {lead_response.text}")
            else:
                print(f"⚠️  No lead capture triggered")
        else:
            print(f"❌ Failed to get response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_lead_creation_without_contact_info():
    """Test creating a lead without contact information"""
    
    print("\n\n📝 Test 2: Interest without Contact Info")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test case 2: User shows interest but no contact info
    test_message = "Je veux acheter un ordinateur portable, combien ça coûte ?"
    
    try:
        response = requests.post(
            f"{base_url}/ai/ask",
            json={"question": test_message},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response received")
            print(f"   - Answer: {data.get('answer', '')[:100]}...")
            print(f"   - Should Capture Lead: {data.get('should_capture_lead', False)}")
            
            # Check contact extraction
            contact_extraction = data.get('contact_extraction', {})
            print(f"   - Contact Extraction:")
            print(f"     * Name: {contact_extraction.get('name', 'None')}")
            print(f"     * Email: {contact_extraction.get('email', 'None')}")
            print(f"     * Phone: {contact_extraction.get('phone', 'None')}")
            print(f"     * Confidence: {contact_extraction.get('confidence', 'None')}")
            
            # Check lead creation
            if data.get('should_capture_lead'):
                lead_id = data.get('preliminary_lead_id')
                lead_status = data.get('lead_status')
                lead_created = data.get('lead_created', False)
                
                print(f"   - Lead Creation:")
                print(f"     * Lead ID: {lead_id}")
                print(f"     * Lead Status: {lead_status}")
                print(f"     * Lead Created: {lead_created}")
                
                # Verify lead in database
                if lead_id:
                    print(f"\n📊 Verifying lead in database...")
                    lead_response = requests.get(f"{base_url}/leads/{lead_id}/messages")
                    
                    if lead_response.status_code == 200:
                        lead_data = lead_response.json()
                        lead_info = lead_data['data']
                        print(f"✅ Lead verified in database:")
                        print(f"   - Name: {lead_info.get('name')}")
                        print(f"   - Email: {lead_info.get('email')}")
                        print(f"   - Phone: {lead_info.get('phone')}")
                        print(f"   - Status: {lead_info.get('status')}")
                    else:
                        print(f"❌ Failed to verify lead: {lead_response.text}")
            else:
                print(f"⚠️  No lead capture triggered")
        else:
            print(f"❌ Failed to get response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_contact_info_update():
    """Test updating lead with contact information in follow-up message"""
    
    print("\n\n📝 Test 3: Contact Info in Follow-up Message")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Step 1: Create lead with interest
    print("Step 1: Creating lead with interest")
    interest_message = "Je veux acheter un ordinateur portable"
    
    try:
        response1 = requests.post(
            f"{base_url}/ai/ask",
            json={"question": interest_message},
            headers={"Content-Type": "application/json"}
        )
        
        if response1.status_code == 200:
            data1 = response1.json()
            lead_id = data1.get('preliminary_lead_id')
            
            if lead_id:
                print(f"✅ Lead created: {lead_id}")
                
                # Step 2: Provide contact info in follow-up
                print(f"\nStep 2: Providing contact info")
                contact_message = "Je m'appelle Marie Martin, mon email est marie.martin@example.com"
                
                response2 = requests.post(
                    f"{base_url}/ai/ask",
                    json={"question": contact_message, "lead_id": lead_id},
                    headers={"Content-Type": "application/json"}
                )
                
                if response2.status_code == 200:
                    data2 = response2.json()
                    print(f"✅ Contact info processed")
                    
                    # Check contact extraction
                    contact_extraction = data2.get('contact_extraction', {})
                    print(f"   - Contact Extraction:")
                    print(f"     * Name: {contact_extraction.get('name', 'None')}")
                    print(f"     * Email: {contact_extraction.get('email', 'None')}")
                    print(f"     * Phone: {contact_extraction.get('phone', 'None')}")
                    print(f"     * Confidence: {contact_extraction.get('confidence', 'None')}")
                    
                    # Check lead update
                    lead_updated = data2.get('lead_updated', False)
                    print(f"   - Lead Updated: {lead_updated}")
                    
                    # Verify updated lead
                    if lead_updated:
                        print(f"\n📊 Verifying updated lead...")
                        lead_response = requests.get(f"{base_url}/leads/{lead_id}/messages")
                        
                        if lead_response.status_code == 200:
                            lead_data = lead_response.json()
                            lead_info = lead_data['data']
                            print(f"✅ Lead updated in database:")
                            print(f"   - Name: {lead_info.get('name')}")
                            print(f"   - Email: {lead_info.get('email')}")
                            print(f"   - Phone: {lead_info.get('phone')}")
                            print(f"   - Status: {lead_info.get('status')}")
                        else:
                            print(f"❌ Failed to verify updated lead: {lead_response.text}")
                else:
                    print(f"❌ Failed to process contact info: {response2.text}")
            else:
                print(f"❌ No lead created")
        else:
            print(f"❌ Failed to create lead: {response1.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Main test function"""
    print("🎯 Lead Creation with Extracted Contact Information Test")
    print("=" * 70)
    
    try:
        # Test 1: Contact info in same message as interest
        test_lead_creation_with_contact_info()
        
        # Test 2: Interest without contact info
        test_lead_creation_without_contact_info()
        
        # Test 3: Contact info in follow-up message
        test_contact_info_update()
        
        print("\n✅ All tests completed!")
        print("\n📋 System Features Demonstrated:")
        print("   - Lead creation with extracted contact information")
        print("   - Automatic contact extraction from user messages")
        print("   - Lead status management based on contact confidence")
        print("   - Lead updates with additional contact information")
        print("   - Message linking to leads")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 