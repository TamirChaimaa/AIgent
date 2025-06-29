#!/usr/bin/env python3
"""
Debug script to test contact extraction directly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.contact_extractor import ContactExtractor

def test_contact_extraction():
    """Test contact extraction with various messages"""
    
    print("🔍 Testing Contact Extraction")
    print("=" * 50)
    
    # Test messages
    test_messages = [
        "Je veux acheter un ordinateur portable. Je m'appelle Jean Dupont, mon email est jean.dupont@example.com et mon téléphone est +33123456789",
        "Je m'appelle Marie Martin, email: marie.martin@test.com, téléphone: 0123456789",
        "Nom: Pierre Durand, Email: pierre.durand@gmail.com, Tél: +33 1 23 45 67 89",
        "Je suis intéressé par un MacBook. Mon nom est Sophie Bernard, mon email sophie.bernard@yahoo.fr et mon téléphone 06 12 34 56 78",
        "Je veux acheter un ordinateur portable"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}:")
        print(f"Message: {message}")
        
        # Extract contact info
        contact_data = ContactExtractor.extract_contact_info(message)
        
        print(f"Extracted data:")
        print(f"  - Name: {contact_data.get('name', 'None')}")
        print(f"  - Email: {contact_data.get('email', 'None')}")
        print(f"  - Phone: {contact_data.get('phone', 'None')}")
        print(f"  - Confidence: {contact_data.get('confidence', 'None')}")
        print(f"  - Method: {contact_data.get('extraction_method', 'None')}")
        
        # Check if it's detected as contact info response
        is_contact_response = ContactExtractor.is_contact_info_response(message)
        print(f"  - Is contact response: {is_contact_response}")

def test_specific_message():
    """Test with the specific message you're using"""
    
    print("\n🎯 Testing Your Specific Message")
    print("=" * 50)
    
    # Replace this with the actual message you're sending
    your_message = "Je veux acheter un ordinateur portable. Je m'appelle Jean Dupont, mon email est jean.dupont@example.com et mon téléphone est +33123456789"
    
    print(f"Your message: {your_message}")
    
    # Extract contact info
    contact_data = ContactExtractor.extract_contact_info(your_message)
    
    print(f"\nExtracted data:")
    print(f"  - Name: {contact_data.get('name', 'None')}")
    print(f"  - Email: {contact_data.get('email', 'None')}")
    print(f"  - Phone: {contact_data.get('phone', 'None')}")
    print(f"  - Confidence: {contact_data.get('confidence', 'None')}")
    
    # Check if it's detected as contact info response
    is_contact_response = ContactExtractor.is_contact_info_response(your_message)
    print(f"  - Is contact response: {is_contact_response}")

if __name__ == "__main__":
    test_contact_extraction()
    test_specific_message() 