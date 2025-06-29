#!/usr/bin/env python3
"""
Test script for English contact extraction
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.contact_extractor import ContactExtractor

def test_english_extraction():
    """Test contact extraction with English messages"""
    
    print("🔍 Testing English Contact Extraction")
    print("=" * 60)
    
    # Test English messages
    english_messages = [
        "I want to buy a laptop. My name is John Smith, my email is john.smith@example.com and my phone is +1234567890",
        "I'm interested in a MacBook. I'm called Mary Johnson, email: mary.johnson@test.com, phone: 555-123-4567",
        "Name: Robert Wilson, Email: robert.wilson@gmail.com, Phone: +1 (555) 987-6543",
        "I am David Brown, my email address is david.brown@yahoo.com and my cell phone is 555-555-5555",
        "Call me Sarah Davis, email: sarah.davis@hotmail.com, mobile: +1-555-123-4567",
        "My name is Michael Johnson, email: michael.johnson@outlook.com, telephone: 555-987-6543"
    ]
    
    for i, message in enumerate(english_messages, 1):
        print(f"\n📝 Test {i}:")
        print(f"Message: {message}")
        
        # Extract contact info
        contact_data = ContactExtractor.extract_contact_info(message)
        
        print(f"Extracted data:")
        print(f"  - Name: {contact_data.get('name', 'None')}")
        print(f"  - Email: {contact_data.get('email', 'None')}")
        print(f"  - Phone: {contact_data.get('phone', 'None')}")
        print(f"  - Confidence: {contact_data.get('confidence', 'None')}")
        
        # Check if it's detected as contact info response
        is_contact_response = ContactExtractor.is_contact_info_response(message)
        print(f"  - Is contact response: {is_contact_response}")

def test_french_vs_english():
    """Compare French and English extraction"""
    
    print("\n\n🌍 Comparing French vs English Extraction")
    print("=" * 60)
    
    # French message
    french_message = "Je veux acheter un ordinateur portable. Je m'appelle Jean Dupont, mon email est jean.dupont@example.com et mon téléphone est +33123456789"
    
    # English message
    english_message = "I want to buy a laptop. My name is John Smith, my email is john.smith@example.com and my phone is +1234567890"
    
    print("🇫🇷 French Message:")
    print(f"Message: {french_message}")
    french_data = ContactExtractor.extract_contact_info(french_message)
    print(f"  - Name: {french_data.get('name', 'None')}")
    print(f"  - Email: {french_data.get('email', 'None')}")
    print(f"  - Phone: {french_data.get('phone', 'None')}")
    print(f"  - Confidence: {french_data.get('confidence', 'None')}")
    
    print("\n🇺🇸 English Message:")
    print(f"Message: {english_message}")
    english_data = ContactExtractor.extract_contact_info(english_message)
    print(f"  - Name: {english_data.get('name', 'None')}")
    print(f"  - Email: {english_data.get('email', 'None')}")
    print(f"  - Phone: {english_data.get('phone', 'None')}")
    print(f"  - Confidence: {english_data.get('confidence', 'None')}")

if __name__ == "__main__":
    test_english_extraction()
    test_french_vs_english() 