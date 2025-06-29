#!/usr/bin/env python3
"""
Simple test script for the new functions
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.interest_analyzer import InterestAnalyzer
from services.contact_extractor import ContactExtractor

def test_detect_serious_interest():
    """Test the detect_serious_interest function"""
    
    print("🎯 Testing detect_serious_interest function")
    print("=" * 50)
    
    test_cases = [
        ("Je veux acheter un ordinateur", True),
        ("I want to buy a laptop", True),
        ("Combien ça coûte ?", True),
        ("How much does it cost?", True),
        ("C'est parfait, je vais le prendre", True),
        ("This looks good, I'll take it", True),
        ("Bonjour, comment allez-vous ?", False),
        ("Hello, how are you?", False),
        ("Pouvez-vous me donner plus d'informations ?", False),
        ("Can you give me more information?", False)
    ]
    
    for message, expected in test_cases:
        result = InterestAnalyzer.detect_serious_interest(message)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"'{message}' -> {result} (expected: {expected}) {status}")

def test_extract_contact_info():
    """Test the extract_contact_info function"""
    
    print("\n\n📞 Testing extract_contact_info function")
    print("=" * 50)
    
    test_cases = [
        "Je m'appelle Jean Dupont, mon email est jean.dupont@example.com et mon téléphone est +33123456789",
        "My name is John Smith, email: john.smith@example.com, phone: +1234567890",
        "Je m'appelle Marie Martin, j'ai 25 ans",
        "My name is Sarah Johnson, I'm 30 years old",
        "Email: test@example.com, Phone: (555) 123-4567",
        "Bonjour, comment allez-vous ?"
    ]
    
    for message in test_cases:
        print(f"\nMessage: {message}")
        try:
            extracted = ContactExtractor.extract_contact_info(message)
            print(f"  Name: {extracted.get('name', 'None')}")
            print(f"  Email: {extracted.get('email', 'None')}")
            print(f"  Phone: {extracted.get('phone', 'None')}")
            print(f"  Age: {extracted.get('age', 'None')}")
            print(f"  Confidence: {extracted.get('confidence', 'None')}")
        except Exception as e:
            print(f"  Error: {e}")

def main():
    """Main test function"""
    print("🧪 Simple Function Tests")
    print("=" * 30)
    
    try:
        test_detect_serious_interest()
        test_extract_contact_info()
        print("\n✅ All tests completed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 