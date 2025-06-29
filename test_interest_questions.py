#!/usr/bin/env python3
"""
Quick test script for interest detection with various questions
"""

import requests
import json

def test_interest_questions():
    """Test different types of questions for interest detection"""
    
    print("🧪 Testing Interest Detection with Various Questions")
    print("=" * 70)
    
    base_url = "http://localhost:5000"
    
    # Test questions categorized by expected interest level
    test_questions = {
        "HIGH INTEREST": [
            "Je veux acheter un ordinateur portable pour le travail",
            "Quel est le prix de vos laptops ?",
            "J'ai besoin d'un ordinateur portable rapidement pour un projet urgent",
            "Est-ce que vous avez des laptops en stock ?",
            "Pouvez-vous me recommander le meilleur ordinateur portable pour le travail ?",
            "Combien coûte votre ordinateur portable le moins cher ?",
            "J'ai un budget de 1000€, que pouvez-vous me proposer ?",
            "Pouvez-vous me livrer un laptop demain ?",
            "Quel laptop me conseillez-vous pour le gaming ?",
            "Aidez-moi à choisir un ordinateur portable"
        ],
        "MEDIUM INTEREST": [
            "Pouvez-vous me montrer vos produits ?",
            "Quels types d'ordinateurs portables vendez-vous ?",
            "Quelles sont les caractéristiques de vos laptops ?",
            "Pouvez-vous me donner plus d'informations sur vos produits ?",
            "Qu'est-ce que vous avez comme ordinateurs portables ?",
            "Pouvez-vous me conseiller sur les ordinateurs portables ?",
            "Quels sont les avantages de vos ordinateurs portables ?",
            "Que me conseillez-vous ?"
        ],
        "LOW INTEREST": [
            "Qu'est-ce que vous vendez ?",
            "Que faites-vous ?",
            "Bonjour, comment allez-vous ?",
            "Quelle est votre adresse ?",
            "Quels sont vos horaires d'ouverture ?",
            "Je regarde juste",
            "Je me renseigne",
            "C'est juste pour voir"
        ]
    }
    
    results = {
        "HIGH INTEREST": {"correct": 0, "total": 0, "details": []},
        "MEDIUM INTEREST": {"correct": 0, "total": 0, "details": []},
        "LOW INTEREST": {"correct": 0, "total": 0, "details": []}
    }
    
    for category, questions in test_questions.items():
        print(f"\n📋 Testing {category} Questions:")
        print("-" * 50)
        
        for i, question in enumerate(questions, 1):
            print(f"\n{i}. {question}")
            
            try:
                response = requests.post(
                    f"{base_url}/ai/ask",
                    json={"question": question},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    interest_analysis = data.get('interest_analysis', {})
                    interest_level = interest_analysis.get('interest_level', 'unknown')
                    interest_score = interest_analysis.get('interest_score', 0)
                    should_capture = interest_analysis.get('should_capture_lead', False)
                    
                    print(f"   - Interest Level: {interest_level}")
                    print(f"   - Interest Score: {interest_score}")
                    print(f"   - Should Capture: {should_capture}")
                    
                    # Determine if result is correct
                    is_correct = False
                    if category == "HIGH INTEREST" and should_capture:
                        is_correct = True
                    elif category == "MEDIUM INTEREST" and (should_capture or interest_level == "medium"):
                        is_correct = True
                    elif category == "LOW INTEREST" and not should_capture:
                        is_correct = True
                    
                    results[category]["total"] += 1
                    if is_correct:
                        results[category]["correct"] += 1
                        print(f"   - ✅ Correct")
                    else:
                        print(f"   - ❌ Incorrect")
                    
                    # Store details
                    results[category]["details"].append({
                        "question": question,
                        "interest_level": interest_level,
                        "interest_score": interest_score,
                        "should_capture": should_capture,
                        "correct": is_correct
                    })
                    
                else:
                    print(f"   - ❌ API Error: {response.status_code}")
                    
            except Exception as e:
                print(f"   - ❌ Error: {str(e)}")
    
    # Print summary
    print(f"\n📊 RESULTS SUMMARY:")
    print("=" * 70)
    
    for category, result in results.items():
        if result["total"] > 0:
            accuracy = (result["correct"] / result["total"]) * 100
            print(f"\n{category}:")
            print(f"   - Correct: {result['correct']}/{result['total']}")
            print(f"   - Accuracy: {accuracy:.1f}%")
            
            # Show incorrect predictions
            incorrect = [d for d in result["details"] if not d["correct"]]
            if incorrect:
                print(f"   - ❌ Incorrect predictions:")
                for item in incorrect:
                    print(f"     • '{item['question'][:50]}...' → {item['interest_level']} (score: {item['interest_score']})")
    
    print(f"\n🎯 Overall System Performance:")
    total_correct = sum(r["correct"] for r in results.values())
    total_questions = sum(r["total"] for r in results.values())
    if total_questions > 0:
        overall_accuracy = (total_correct / total_questions) * 100
        print(f"   - Total Accuracy: {overall_accuracy:.1f}%")
        print(f"   - Correct Predictions: {total_correct}/{total_questions}")

def test_specific_scenarios():
    """Test specific scenarios that should work well"""
    
    print(f"\n🎯 Testing Specific Scenarios:")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    scenarios = [
        {
            "name": "Direct Purchase Intent",
            "question": "Je veux acheter un ordinateur portable maintenant",
            "expected": "high"
        },
        {
            "name": "Price Inquiry",
            "question": "Combien coûte votre laptop le moins cher ?",
            "expected": "high"
        },
        {
            "name": "Urgency",
            "question": "J'ai besoin d'un ordinateur rapidement",
            "expected": "high"
        },
        {
            "name": "Stock Check",
            "question": "Avez-vous des laptops en stock ?",
            "expected": "high"
        },
        {
            "name": "General Inquiry",
            "question": "Que vendez-vous ?",
            "expected": "low"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📝 {scenario['name']}: {scenario['question']}")
        
        try:
            response = requests.post(
                f"{base_url}/ai/ask",
                json={"question": scenario['question']},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                interest_level = data.get('interest_analysis', {}).get('interest_level', 'unknown')
                should_capture = data.get('should_capture_lead', False)
                
                print(f"   - Expected: {scenario['expected']}")
                print(f"   - Got: {interest_level}")
                print(f"   - Should Capture: {should_capture}")
                
                if interest_level == scenario['expected']:
                    print(f"   - ✅ Correct prediction")
                else:
                    print(f"   - ❌ Incorrect prediction")
                    
            else:
                print(f"   - ❌ API Error")
                
        except Exception as e:
            print(f"   - ❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Interest Detection Tests")
    print("Make sure your Flask server is running on http://localhost:5000")
    print("=" * 70)
    
    try:
        test_interest_questions()
        test_specific_scenarios()
        
        print(f"\n✅ All tests completed!")
        print(f"\n💡 Tips:")
        print(f"   - High interest questions should trigger lead capture")
        print(f"   - Medium interest questions may trigger lead capture")
        print(f"   - Low interest questions should NOT trigger lead capture")
        print(f"   - The system uses AI + keyword analysis for detection")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc() 