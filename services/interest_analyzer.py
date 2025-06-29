import re
from typing import Dict, List, Tuple, Optional
import json
from services.ai_services import AiService

class InterestAnalyzer:
    def __init__(self):
        self.ai_service = AiService()
    
    # Mots-clés de base (fallback si l'IA n'est pas disponible)
    BASE_HIGH_INTEREST_KEYWORDS = [
        "acheter", "commander", "prix", "coût", "combien", "disponible", "stock",
        "buy", "order", "price", "cost", "how much", "available", "in stock",
        "livraison", "delivery", "expédition", "shipping", "garantie", "warranty",
        "spécifications", "specifications", "détails", "details", "comparer", "compare",
        "meilleur", "best", "recommandé", "recommended", "populaire", "popular",
        "promotion", "réduction", "discount", "offre", "deal", "solde", "sale"
    ]
    
    BASE_PURCHASE_INTENT_KEYWORDS = [
        "je veux", "i want", "j'aimerais", "i would like", "je cherche", "i'm looking for",
        "peux-tu me montrer", "can you show me", "montrez-moi", "show me",
        "quels sont les", "what are the", "donnez-moi", "give me",
        "je voudrais acheter", "i want to buy", "je souhaite", "i wish",
        "aide-moi à choisir", "help me choose", "conseillez-moi", "advise me"
    ]
    
    @staticmethod
    def generate_ai_keywords(question: str, context: str = "") -> Dict:
        """
        Use AI to generate dynamic keywords for interest analysis
        """
        prompt = f"""
        Analyze this customer question and generate keywords that indicate purchase intent and interest level.
        
        Customer Question: "{question}"
        Context: {context}
        
        Please return a JSON object with the following structure:
        {{
            "high_interest_keywords": ["keyword1", "keyword2", ...],
            "purchase_intent_keywords": ["intent1", "intent2", ...],
            "urgency_indicators": ["urgent1", "urgent2", ...],
            "interest_score": 0-10,
            "confidence_level": "low/medium/high",
            "reasoning": "explanation of why these keywords were chosen"
        }}
        
        Focus on:
        1. Words that show buying intention
        2. Words that indicate urgency
        3. Words that show product interest
        4. Words that indicate price sensitivity
        5. Words that show comparison shopping behavior
        """
        
        try:
            ai_service = AiService()
            response = ai_service.ask_question(prompt)
            
            # The response is a dict with 'message' and 'products' keys
            if isinstance(response, dict) and 'message' in response:
                response_text = response['message']
                
                # Try to parse JSON from response text
                if response_text and "{" in response_text and "}" in response_text:
                    # Extract JSON from response
                    json_start = response_text.find("{")
                    json_end = response_text.rfind("}") + 1
                    json_str = response_text[json_start:json_end]
                    
                    keywords_data = json.loads(json_str)
                    return keywords_data
                else:
                    # Fallback to base keywords
                    return {
                        "high_interest_keywords": InterestAnalyzer.BASE_HIGH_INTEREST_KEYWORDS,
                        "purchase_intent_keywords": InterestAnalyzer.BASE_PURCHASE_INTENT_KEYWORDS,
                        "urgency_indicators": ["urgent", "rapidement", "quickly", "maintenant", "now"],
                        "interest_score": 0,
                        "confidence_level": "low",
                        "reasoning": "Using fallback keywords"
                    }
            else:
                # Fallback to base keywords
                return {
                    "high_interest_keywords": InterestAnalyzer.BASE_HIGH_INTEREST_KEYWORDS,
                    "purchase_intent_keywords": InterestAnalyzer.BASE_PURCHASE_INTENT_KEYWORDS,
                    "urgency_indicators": ["urgent", "rapidement", "quickly", "maintenant", "now"],
                    "interest_score": 0,
                    "confidence_level": "low",
                    "reasoning": "Using fallback keywords"
                }
        except Exception as e:
            print(f"Error generating AI keywords: {e}")
            return {
                "high_interest_keywords": InterestAnalyzer.BASE_HIGH_INTEREST_KEYWORDS,
                "purchase_intent_keywords": InterestAnalyzer.BASE_PURCHASE_INTENT_KEYWORDS,
                "urgency_indicators": ["urgent", "rapidement", "quickly", "maintenant", "now"],
                "interest_score": 0,
                "confidence_level": "low",
                "reasoning": f"Error: {str(e)}"
            }
    
    @staticmethod
    def analyze_interest_with_ai(question: str, answer: str, products: List[Dict]) -> Dict:
        """
        Analyze interest using AI-generated keywords and patterns
        """
        question_lower = question.lower()
        answer_lower = answer.lower()
        
        # Generate AI keywords
        ai_keywords = InterestAnalyzer.generate_ai_keywords(question, f"AI Answer: {answer}")
        
        # Calculate interest score using AI-generated keywords
        interest_score = 0
        interest_reasons = []
        
        # Use AI-generated high interest keywords
        for keyword in ai_keywords.get("high_interest_keywords", []):
            if keyword.lower() in question_lower:
                interest_score += 2
                interest_reasons.append(f"AI Keyword: {keyword}")
        
        # Use AI-generated purchase intent keywords
        for keyword in ai_keywords.get("purchase_intent_keywords", []):
            if keyword.lower() in question_lower:
                interest_score += 3
                interest_reasons.append(f"AI Purchase Intent: {keyword}")
        
        # Use AI-generated urgency indicators
        for indicator in ai_keywords.get("urgency_indicators", []):
            if indicator.lower() in question_lower:
                interest_score += 3
                interest_reasons.append(f"AI Urgency: {indicator}")
        
        # Add AI-generated base score
        ai_base_score = ai_keywords.get("interest_score", 0)
        interest_score += ai_base_score
        if ai_base_score > 0:
            interest_reasons.append(f"AI Base Score: {ai_base_score}")
        
        # Check if products were recommended
        if products and len(products) > 0:
            interest_score += 2
            interest_reasons.append(f"Products recommended: {len(products)}")
        
        # Check for follow-up questions
        if "?" in question:
            interest_score += 1
            interest_reasons.append("Question asked")
        
        # Determine interest level
        interest_level = "low"
        should_capture_lead = False
        
        if interest_score >= 8:
            interest_level = "high"
            should_capture_lead = True
        elif interest_score >= 5:
            interest_level = "medium"
            should_capture_lead = True
        elif interest_score >= 3:
            interest_level = "low"
            should_capture_lead = False
        
        return {
            "interest_score": interest_score,
            "interest_level": interest_level,
            "should_capture_lead": should_capture_lead,
            "interest_reasons": interest_reasons,
            "recommended_products": [p.get("name", "") for p in products] if products else [],
            "ai_analysis": {
                "confidence_level": ai_keywords.get("confidence_level", "low"),
                "reasoning": ai_keywords.get("reasoning", ""),
                "generated_keywords": ai_keywords
            }
        }
    
    @staticmethod
    def analyze_interest_level(question: str, answer: str, products: List[Dict]) -> Dict:
        """
        Main method - uses AI-enhanced analysis with fallback to traditional method
        """
        try:
            # Try AI-enhanced analysis first
            return InterestAnalyzer.analyze_interest_with_ai(question, answer, products)
        except Exception as e:
            print(f"AI analysis failed, using fallback: {e}")
            # Fallback to original method
            return InterestAnalyzer._analyze_interest_fallback(question, answer, products)
    
    @staticmethod
    def _analyze_interest_fallback(question: str, answer: str, products: List[Dict]) -> Dict:
        """
        Fallback analysis method using predefined keywords
        """
        question_lower = question.lower()
        answer_lower = answer.lower()
        
        # Calculate interest score
        interest_score = 0
        interest_reasons = []
        
        # Check for high interest keywords
        for keyword in InterestAnalyzer.BASE_HIGH_INTEREST_KEYWORDS:
            if keyword in question_lower:
                interest_score += 2
                interest_reasons.append(f"Keyword: {keyword}")
        
        # Check for purchase intent keywords
        for keyword in InterestAnalyzer.BASE_PURCHASE_INTENT_KEYWORDS:
            if keyword in question_lower:
                interest_score += 3
                interest_reasons.append(f"Purchase intent: {keyword}")
        
        # Check for urgency indicators
        urgency_indicators = ["urgent", "rapidement", "quickly", "maintenant", "now", "tout de suite", "immediately"]
        for indicator in urgency_indicators:
            if indicator in question_lower:
                interest_score += 3
                interest_reasons.append(f"Urgency: {indicator}")
        
        # Check if products were recommended
        if products and len(products) > 0:
            interest_score += 2
            interest_reasons.append(f"Products recommended: {len(products)}")
        
        # Check for follow-up questions
        if "?" in question:
            interest_score += 1
            interest_reasons.append("Question asked")
        
        # Determine interest level
        interest_level = "low"
        should_capture_lead = False
        
        if interest_score >= 8:
            interest_level = "high"
            should_capture_lead = True
        elif interest_score >= 5:
            interest_level = "medium"
            should_capture_lead = True
        elif interest_score >= 3:
            interest_level = "low"
            should_capture_lead = False
        
        return {
            "interest_score": interest_score,
            "interest_level": interest_level,
            "should_capture_lead": should_capture_lead,
            "interest_reasons": interest_reasons,
            "recommended_products": [p.get("name", "") for p in products] if products else [],
            "ai_analysis": {
                "confidence_level": "low",
                "reasoning": "Using fallback analysis",
                "generated_keywords": {}
            }
        }
    
    @staticmethod
    def generate_lead_capture_message(interest_analysis: Dict) -> Optional[str]:
        """
        Generate a friendly message to capture lead information
        """
        if not interest_analysis.get("should_capture_lead"):
            return None
        
        interest_level = interest_analysis.get("interest_level", "medium")
        products = interest_analysis.get("recommended_products", [])
        
        if interest_level == "high":
            message = "🎉 Excellent ! Je vois que vous êtes très intéressé par nos produits ! "
            message += "Pour vous offrir le meilleur service et vous tenir informé des promotions, "
            message += "j'aurais besoin de quelques informations :\n\n"
            message += "📝 **Vos coordonnées :**\n"
            message += "• Votre nom complet :\n"
            message += "• Votre adresse email :\n"
            message += "• Votre numéro de téléphone :\n\n"
            message += "Une fois ces informations fournies, je pourrai :\n"
            message += "✅ Vous envoyer des offres personnalisées\n"
            message += "✅ Vous contacter pour un suivi personnalisé\n"
            message += "✅ Vous informer des nouvelles promotions\n"
            message += "✅ Répondre à toutes vos questions en détail"
        else:
            message = "👍 Je vois que vous appréciez nos produits ! "
            message += "Pour vous envoyer des informations personnalisées et des offres exclusives, "
            message += "pourriez-vous me donner vos coordonnées ?\n\n"
            message += "📝 **Informations nécessaires :**\n"
            message += "• Nom :\n"
            message += "• Email :\n"
            message += "• Téléphone :\n\n"
            message += "Cela me permettra de mieux vous servir !"
        
        if products:
            product_names = ", ".join(products[:3])  # Show first 3 products
            message += f"\n\n📦 **Produits qui vous intéressent :** {product_names}"
        
        message += "\n\n💬 **Répondez simplement avec vos informations ci-dessus !**"
        
        return message
    
    @staticmethod
    def extract_product_names_from_question(question: str) -> List[str]:
        """
        Extract potential product names from the user's question
        """
        # This is a simple extraction - you could make it more sophisticated
        # by comparing against your actual product database
        words = question.split()
        potential_products = []
        
        # Look for capitalized words that might be product names
        for word in words:
            if word[0].isupper() and len(word) > 2:
                potential_products.append(word)
        
        return potential_products 