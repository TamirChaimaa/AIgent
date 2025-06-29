from services.interest_analyzer import InterestAnalyzer

def test_interest_detection():
    """Test simple de la détection d'intérêt"""
    
    print("🔍 TEST DE DÉTECTION D'INTÉRÊT")
    print("=" * 40)
    
    # Questions de test
    test_questions = [
        "Combien coûte le MacBook Air M2 ? Je veux l'acheter rapidement",
        "Bonjour, comment allez-vous ?",
        "Montrez-moi les laptops disponibles",
        "Quel est le prix du Dell XPS 13 ? Je suis très intéressé",
        "Merci pour l'information",
        "Je voudrais acheter un ordinateur portable, pouvez-vous me recommander ?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: '{question}'")
        
        # Analyser l'intérêt
        analysis = InterestAnalyzer.analyze_interest_level(
            question=question,
            answer="Réponse de l'AI",
            products=[]
        )
        
        print(f"   📊 Score: {analysis['interest_score']}")
        print(f"   🎯 Niveau: {analysis['interest_level']}")
        print(f"   📝 Capture lead: {analysis['should_capture_lead']}")
        
        if analysis['interest_reasons']:
            print(f"   🔍 Raisons: {', '.join(analysis['interest_reasons'])}")
        
        if analysis['should_capture_lead']:
            message = InterestAnalyzer.generate_lead_capture_message(analysis)
            print(f"   💬 Message: {message[:80]}...")
        
        print("-" * 40)

if __name__ == "__main__":
    test_interest_detection() 