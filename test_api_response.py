#!/usr/bin/env python3
"""
Simple test to verify API response includes lead capture message
"""

import requests
import json

def test_api_response():
    """Test if the API correctly returns lead capture message"""
    
    print("🧪 Testing API Response for Lead Capture")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test question that should trigger lead capture
    test_question = "Je veux acheter un ordinateur portable"
    
    print(f"📝 Testing question: '{test_question}'")
    print("-" * 50)
    
    try:
        # Send request to API
        response = requests.post(
            f"{base_url}/ai/ask",
            json={"question": test_question},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📡 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n📊 Response Analysis:")
            print(f"   - Question: {data.get('question', 'N/A')}")
            print(f"   - Answer: {data.get('answer', 'N/A')[:100]}...")
            
            # Check interest analysis
            interest_analysis = data.get('interest_analysis', {})
            print(f"   - Interest Level: {interest_analysis.get('interest_level', 'N/A')}")
            print(f"   - Interest Score: {interest_analysis.get('interest_score', 'N/A')}")
            print(f"   - Should Capture Lead: {interest_analysis.get('should_capture_lead', 'N/A')}")
            
            # Check lead capture message
            lead_capture_message = data.get('lead_capture_message')
            should_capture = data.get('should_capture_lead', False)
            
            print(f"\n🎯 Lead Capture Results:")
            print(f"   - Should Capture: {should_capture}")
            
            if lead_capture_message:
                print(f"   - ✅ Lead Capture Message Found:")
                print(f"   - Message: {lead_capture_message[:200]}...")
                print(f"   - Message Length: {len(lead_capture_message)} characters")
            else:
                print(f"   - ❌ No Lead Capture Message Found")
            
            # Check preliminary lead ID
            preliminary_lead_id = data.get('preliminary_lead_id')
            if preliminary_lead_id:
                print(f"   - ✅ Preliminary Lead ID: {preliminary_lead_id}")
            else:
                print(f"   - ❌ No Preliminary Lead ID")
            
            # Check message ID
            message_id = data.get('message_id')
            if message_id:
                print(f"   - ✅ Message ID: {message_id}")
            
            print(f"\n📋 Full Response Keys:")
            for key in data.keys():
                print(f"   - {key}: {type(data[key]).__name__}")
            
            # Test conclusion
            if should_capture and lead_capture_message:
                print(f"\n✅ SUCCESS: API correctly returns lead capture message")
                print(f"   The frontend should display the lead capture message")
            elif should_capture and not lead_capture_message:
                print(f"\n❌ PROBLEM: Should capture lead but no message found")
                print(f"   Check the InterestAnalyzer.generate_lead_capture_message() function")
            elif not should_capture:
                print(f"\n⚠️  INFO: No lead capture triggered (interest too low)")
                print(f"   This is normal for low-interest questions")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_multiple_questions():
    """Test multiple questions to see which trigger lead capture"""
    
    print(f"\n🔄 Testing Multiple Questions")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    test_questions = [
        {
            "question": "Je veux acheter un ordinateur portable",
            "expected": "high"
        },
        {
            "question": "Quel est le prix de vos laptops ?",
            "expected": "high"
        },
        {
            "question": "Qu'est-ce que vous vendez ?",
            "expected": "low"
        }
    ]
    
    for i, test_case in enumerate(test_questions, 1):
        print(f"\n📝 Test {i}: {test_case['question']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                f"{base_url}/ai/ask",
                json={"question": test_case['question']},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                interest_level = data.get('interest_analysis', {}).get('interest_level', 'unknown')
                should_capture = data.get('should_capture_lead', False)
                has_message = bool(data.get('lead_capture_message'))
                
                print(f"   - Expected: {test_case['expected']}")
                print(f"   - Got: {interest_level}")
                print(f"   - Should Capture: {should_capture}")
                print(f"   - Has Message: {has_message}")
                
                if should_capture and has_message:
                    print(f"   - ✅ Lead capture message available")
                elif should_capture and not has_message:
                    print(f"   - ❌ Missing lead capture message")
                else:
                    print(f"   - ⚠️  No lead capture (expected)")
                    
            else:
                print(f"   - ❌ API Error: {response.status_code}")
                
        except Exception as e:
            print(f"   - ❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Testing API Response for Lead Capture")
    print("Make sure your Flask server is running on http://localhost:5000")
    print("=" * 60)
    
    try:
        test_api_response()
        test_multiple_questions()
        
        print(f"\n✅ Test completed!")
        print(f"\n💡 If the API returns lead_capture_message but the frontend doesn't show it:")
        print(f"   - Check your frontend code for displaying lead_capture_message")
        print(f"   - Make sure the frontend handles the should_capture_lead field")
        print(f"   - Verify the frontend displays the message when should_capture_lead is true")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc() 