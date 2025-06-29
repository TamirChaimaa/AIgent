#!/usr/bin/env python3
"""
Simple test for contact extraction
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.contact_extractor import ContactExtractor

def test_extraction():
    print("🔍 Testing Contact Extraction")
    print("=" * 50)
    
    # Test message
    test_message = "Je veux acheter un ordinateur portable. Je m'appelle Jean Dupont, mon email est jean.dupont@example.com et mon téléphone est +33123456789"
    
    print(f"Message: {test_message}")
    print()
    
    # Extract contact info
    contact_data = ContactExtractor.extract_contact_info(test_message)
    
    print(f"Extracted data:")
    print(f"  - Name: {contact_data.get('name', 'None')}")
    print(f"  - Email: {contact_data.get('email', 'None')}")
    print(f"  - Phone: {contact_data.get('phone', 'None')}")
    print(f"  - Confidence: {contact_data.get('confidence', 'None')}")
    
    # Check if it's detected as contact info response
    is_contact_response = ContactExtractor.is_contact_info_response(test_message)
    print(f"  - Is contact response: {is_contact_response}")

if __name__ == "__main__":
    test_extraction() 