#!/usr/bin/env python3
"""
Test script for AI-powered interest analysis
Demonstrates how the AI generates dynamic keywords for interest detection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.interest_analyzer import InterestAnalyzer

def test_ai_keyword_generation():
    """Test AI keyword generation for different types of questions"""
    
    print("🤖 Testing AI-Powered Interest Analysis")
    print("=" * 50)
    
    # Test questions with different interest levels
    test_questions = [
        {
            "question": "Je veux acheter un ordinateur portable pour le travail, pouvez-vous me recommander quelque chose ?",
            "expected_level": "high"
        },
        {
            "question": "Quel est le prix de vos laptops ?",
            "expected_level": "high"
        },
        {
            "question": "J'ai besoin d'un ordinateur rapidement pour un projet urgent",
            "expected_level": "high"
        },
        {
            "question": "Pouvez-vous me montrer vos produits ?",
            "expected_level": "medium"
        },
        {
            "question": "Qu'est-ce que vous vendez ?",
            "expected_level": "low"
        },
        {
            "question": "I want to buy a laptop for gaming, what do you recommend?",
            "expected_level": "high"
        },
        {
            "question": "How much does your cheapest laptop cost?",
            "expected_level": "high"
        },
        {
            "question": "Can you show me your products?",
            "expected_level": "medium"
        }
    ]
    
    analyzer = InterestAnalyzer()
    
    for i, test_case in enumerate(test_questions, 1):
        question = test_case["question"]
        expected = test_case["expected_level"]
        
        print(f"\n📝 Test {i}: {question}")
        print("-" * 40)
        
        try:
            # Test AI keyword generation
            print("🔍 Generating AI keywords...")
            ai_keywords = InterestAnalyzer.generate_ai_keywords(question)
            
            print(f"✅ AI Keywords Generated:")
            print(f"   - High Interest: {ai_keywords.get('high_interest_keywords', [])[:3]}...")
            print(f"   - Purchase Intent: {ai_keywords.get('purchase_intent_keywords', [])[:3]}...")
            print(f"   - Urgency: {ai_keywords.get('urgency_indicators', [])[:3]}...")
            print(f"   - AI Score: {ai_keywords.get('interest_score', 0)}")
            print(f"   - Confidence: {ai_keywords.get('confidence_level', 'low')}")
            print(f"   - Reasoning: {ai_keywords.get('reasoning', 'N/A')[:100]}...")
            
            # Test full interest analysis
            print("\n🎯 Full Interest Analysis:")
            analysis = InterestAnalyzer.analyze_interest_level(
                question, 
                "Voici nos recommandations...", 
                [{"name": "Laptop Pro", "price": 999}]
            )
            
            print(f"   - Interest Score: {analysis['interest_score']}")
            print(f"   - Interest Level: {analysis['interest_level']}")
            print(f"   - Should Capture Lead: {analysis['should_capture_lead']}")
            print(f"   - Reasons: {analysis['interest_reasons'][:3]}...")
            
            # Check if AI analysis was used
            ai_analysis = analysis.get('ai_analysis', {})
            if ai_analysis.get('confidence_level') != 'low':
                print(f"   - ✅ AI Analysis Used: {ai_analysis.get('confidence_level')}")
            else:
                print(f"   - ⚠️  Fallback Analysis Used")
            
            # Test lead capture message
            if analysis['should_capture_lead']:
                lead_message = InterestAnalyzer.generate_lead_capture_message(analysis)
                if lead_message:
                    print(f"   - 📧 Lead Message: {lead_message[:100]}...")
            
            # Verify expected level
            if analysis['interest_level'] == expected:
                print(f"   - ✅ Expected Level: {expected} ✓")
            else:
                print(f"   - ❌ Expected: {expected}, Got: {analysis['interest_level']}")
                
        except Exception as e:
            print(f"   - ❌ Error: {str(e)}")
        
        print()

def test_ai_vs_fallback():
    """Compare AI analysis vs fallback analysis"""
    
    print("\n🔄 Comparing AI vs Fallback Analysis")
    print("=" * 50)
    
    question = "Je veux acheter un ordinateur portable pour le travail, pouvez-vous me recommander quelque chose ?"
    
    print(f"Question: {question}")
    print("-" * 40)
    
    try:
        # Test AI analysis
        print("🤖 AI Analysis:")
        ai_analysis = InterestAnalyzer.analyze_interest_with_ai(
            question, 
            "Voici nos recommandations...", 
            [{"name": "Laptop Pro", "price": 999}]
        )
        
        print(f"   - Score: {ai_analysis['interest_score']}")
        print(f"   - Level: {ai_analysis['interest_level']}")
        print(f"   - AI Confidence: {ai_analysis['ai_analysis']['confidence_level']}")
        print(f"   - AI Reasoning: {ai_analysis['ai_analysis']['reasoning'][:100]}...")
        
        # Test fallback analysis
        print("\n📋 Fallback Analysis:")
        fallback_analysis = InterestAnalyzer._analyze_interest_fallback(
            question, 
            "Voici nos recommandations...", 
            [{"name": "Laptop Pro", "price": 999}]
        )
        
        print(f"   - Score: {fallback_analysis['interest_score']}")
        print(f"   - Level: {fallback_analysis['interest_level']}")
        print(f"   - Using predefined keywords")
        
        # Compare results
        print(f"\n📊 Comparison:")
        print(f"   - AI Score: {ai_analysis['interest_score']} vs Fallback: {fallback_analysis['interest_score']}")
        print(f"   - AI Level: {ai_analysis['interest_level']} vs Fallback: {fallback_analysis['interest_level']}")
        
        if ai_analysis['interest_score'] > fallback_analysis['interest_score']:
            print(f"   - ✅ AI provided higher score")
        elif ai_analysis['interest_score'] < fallback_analysis['interest_score']:
            print(f"   - ⚠️  Fallback provided higher score")
        else:
            print(f"   - ➖ Same score")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Main test function"""
    print("🚀 Starting AI Interest Analysis Tests")
    print("=" * 60)
    
    try:
        # Test AI keyword generation
        test_ai_keyword_generation()
        
        # Test AI vs fallback comparison
        test_ai_vs_fallback()
        
        print("\n✅ All tests completed!")
        print("\n💡 Key Benefits of AI-Powered Analysis:")
        print("   - Dynamic keyword generation based on context")
        print("   - Adapts to different languages and expressions")
        print("   - Provides reasoning for interest detection")
        print("   - Fallback to predefined keywords if AI fails")
        print("   - More accurate interest scoring")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 