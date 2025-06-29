#!/usr/bin/env python3
"""
Test script to check lead creation consistency
"""

import requests
import json
import time

def test_lead_creation_consistency():
    """Test lead creation multiple times to check consistency"""
    
    print("🎯 Testing Lead Creation Consistency")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test message that should trigger lead creation
    test_message = "Je veux acheter un ordinateur portable. Je m'appelle Jean Dupont, mon email est jean.dupont@example.com et mon téléphone est +33123456789"
    
    for i in range(3):
        print(f"\n📝 Test {i+1}:")
        
        try:
            response = requests.post(
                f"{base_url}/ai/ask",
                json={"question": test_message},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Response received")
                print(f"   - Should Capture Lead: {data.get('should_capture_lead', False)}")
                print(f"   - Lead Created: {data.get('lead_created', False)}")
                print(f"   - Lead ID: {data.get('preliminary_lead_id', 'None')}")
                
                # Check contact extraction
                contact_extraction = data.get('contact_extraction', {})
                print(f"   - Contact Extraction:")
                print(f"     * Name: {contact_extraction.get('name', 'None')}")
                print(f"     * Email: {contact_extraction.get('email', 'None')}")
                print(f"     * Phone: {contact_extraction.get('phone', 'None')}")
                print(f"     * Confidence: {contact_extraction.get('confidence', 'None')}")
                
                # Check interest analysis
                interest_analysis = data.get('interest_analysis', {})
                print(f"   - Interest Analysis:")
                print(f"     * Should Capture: {interest_analysis.get('should_capture_lead', False)}")
                print(f"     * Serious Interest: {interest_analysis.get('serious_interest_detected', False)}")
                print(f"     * Combined Should Capture: {interest_analysis.get('combined_should_capture', False)}")
                
            else:
                print(f"❌ Failed to get response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Wait a bit between tests
        time.sleep(1)

def test_different_messages():
    """Test with different messages to see which ones create leads"""
    
    print("\n\n🎯 Testing Different Messages")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    test_messages = [
        "Je veux acheter un ordinateur portable. Je m'appelle Jean Dupont, mon email est jean.dupont@example.com et mon téléphone est +33123456789",
        "Je suis intéressé par un MacBook Air M2",
        "Combien coûte un ordinateur portable ?",
        "Je veux acheter un ordinateur portable. Je m'appelle Marie Martin, email: marie.martin@test.com"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test Message {i}:")
        print(f"Message: {message[:50]}...")
        
        try:
            response = requests.post(
                f"{base_url}/ai/ask",
                json={"question": message},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                should_capture = data.get('should_capture_lead', False)
                lead_created = data.get('lead_created', False)
                lead_id = data.get('preliminary_lead_id', 'None')
                
                print(f"   - Should Capture: {should_capture}")
                print(f"   - Lead Created: {lead_created}")
                print(f"   - Lead ID: {lead_id}")
                
            else:
                print(f"   - Failed: {response.text}")
                
        except Exception as e:
            print(f"   - Error: {str(e)}")

if __name__ == "__main__":
    test_lead_creation_consistency()
    test_different_messages() 