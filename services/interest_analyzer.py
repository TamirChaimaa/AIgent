import re
from typing import Dict, List, Tuple, Optional
import json
from services.ai_services import AiService

class InterestAnalyzer:
    def __init__(self):
        self.ai_service = AiService()
    
    # Base keywords (fallback if AI is unavailable)
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
    def detect_serious_interest(user_message: str) -> bool:
        """
        Detect if customer shows serious interest in purchasing
        """
        interest_keywords = [
            "buy", "purchase", "order", "get this", "take it", "want this",
            "interested in", "looks good", "perfect", "exactly what", 
            "how much", "price", "cost", "afford", "budget", "payment",
            "when can i", "available", "in stock", "reserve", "hold",
            "size", "fit", "try on", "store location", "pickup", "delivery",
            "want", "take", "want to buy", "want to order",
            "like", "like to buy", "like to order",
            "love", "love to buy", "love to order",
            "need", "need to buy", "need to order",
   
            # French equivalents
            "acheter", "commander", "prendre", "vouloir", "intéressé par",
            "parfait", "exactement", "combien", "prix", "coût", "budget",
            "disponible", "en stock", "réserver", "livraison", "retrait"
            "taille", "tenir", "essayer", "magasin", "emporter", "livraison",
            "veux", "prendre", "veux acheter", "veux commander",
            "aime", "aime acheter", "aime commander",
            "adore", "adore acheter", "adore commander",
            "besoin", "besoin acheter", "besoin commander",
        ]
        
        message_lower = user_message.lower()
        interest_count = sum(1 for keyword in interest_keywords if keyword in message_lower)
        
        serious_phrases = [
            "i want", "i'll take", "can i buy", "how do i order", 
            "where can i", "i need these", "perfect for me",
            # French equivalents
            "je veux", "je vais prendre", "peux-je acheter", "comment commander",
            "où puis-je", "j'ai besoin", "parfait pour moi"
        ]
        
        return interest_count >= 2 or any(phrase in message_lower for phrase in serious_phrases)
    
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
        
        ai_keywords = InterestAnalyzer.generate_ai_keywords(question, f"AI Answer: {answer}")
        interest_score = 0
        interest_reasons = []
        
        for keyword in ai_keywords.get("high_interest_keywords", []):
            if keyword.lower() in question_lower:
                interest_score += 2
                interest_reasons.append(f"AI Keyword: {keyword}")
        
        for keyword in ai_keywords.get("purchase_intent_keywords", []):
            if keyword.lower() in question_lower:
                interest_score += 3
                interest_reasons.append(f"AI Purchase Intent: {keyword}")
        
        for indicator in ai_keywords.get("urgency_indicators", []):
            if indicator.lower() in question_lower:
                interest_score += 3
                interest_reasons.append(f"AI Urgency: {indicator}")
        
        ai_base_score = ai_keywords.get("interest_score", 0)
        interest_score += ai_base_score
        if ai_base_score > 0:
            interest_reasons.append(f"AI Base Score: {ai_base_score}")
        
        if products and len(products) > 0:
            interest_score += 2
            interest_reasons.append(f"Products recommended: {len(products)}")
        
        if "?" in question:
            interest_score += 1
            interest_reasons.append("Question asked")
        
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
            return InterestAnalyzer.analyze_interest_with_ai(question, answer, products)
        except Exception as e:
            print(f"AI analysis failed, using fallback: {e}")
            return InterestAnalyzer._analyze_interest_fallback(question, answer, products)
    
    @staticmethod
    def _analyze_interest_fallback(question: str, answer: str, products: List[Dict]) -> Dict:
        """
        Fallback analysis method using predefined keywords
        """
        question_lower = question.lower()
        answer_lower = answer.lower()
        
        interest_score = 0
        interest_reasons = []
        
        for keyword in InterestAnalyzer.BASE_HIGH_INTEREST_KEYWORDS:
            if keyword in question_lower:
                interest_score += 2
                interest_reasons.append(f"Keyword: {keyword}")
        
        for keyword in InterestAnalyzer.BASE_PURCHASE_INTENT_KEYWORDS:
            if keyword in question_lower:
                interest_score += 3
                interest_reasons.append(f"Purchase intent: {keyword}")
        
        urgency_indicators = ["urgent", "rapidement", "quickly", "maintenant", "now", "tout de suite", "immediately"]
        for indicator in urgency_indicators:
            if indicator in question_lower:
                interest_score += 3
                interest_reasons.append(f"Urgency: {indicator}")
        
        if products and len(products) > 0:
            interest_score += 2
            interest_reasons.append(f"Products recommended: {len(products)}")
        
        if "?" in question:
            interest_score += 1
            interest_reasons.append("Question asked")
        
        interest_level = "low"
        should_capture_lead = False
        
        if interest_score >= 10:
            interest_level = "high"
            should_capture_lead = True
        elif interest_score >= 7:
            interest_level = "medium"
            should_capture_lead = True
        elif interest_score >= 5:
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
    def generate_lead_capture_message(interest_analysis: Dict, user_message: Optional[str] = None) -> Optional[str]:
      """
       Generate lead capture message only if no contact info already exists in user message.
       """
      if not interest_analysis.get("should_capture_lead"):
        return None

      if user_message:
        contact_info = InterestAnalyzer.extract_contact_info(user_message)
        if contact_info.get("email") or contact_info.get("phone"):
            return None  # Ne pas générer de message si coordonnées déjà présentes

      interest_level = interest_analysis.get("interest_level", "medium")
      products = interest_analysis.get("recommended_products", [])

      product_names = ", ".join(products[:3]) if products else ""
      message = ""

      if interest_level == "high":
        message += "🎉 Excellent! I see you're very interested in our products"
        if product_names:
            message += f" like {product_names}"
        message += "! To offer you the best service and keep you informed of promotions, "
        message += "I'd need a few details from you:\n\n"
        message += "📝 **Your contact info:**\n"
        message += "• Full name:\n"
        message += "• Email address:\n"
        message += "• Phone number:\n\n"
        message += "Once we have this, I can:\n"
        message += "✅ Send you personalized offers\n"
        message += "✅ Contact you for personalized follow-up\n"
        message += "✅ Inform you about new promotions\n"
        message += "✅ Answer all your questions in detail\n"
        message += "\n💬 **Just reply with your information above!**"

      elif interest_level == "medium":
        message += "😊 Great! I see you're interested"
        if product_names:
            message += f" in {product_names}"
        message += ". Could you please share your contact details so we can follow up?\n"
        message += "📝 **Your contact info:**\n"
        message += "• Full name:\n"
        message += "• Email address:\n"
        message += "• Phone number:\n"
        message += "\n💬 **Just reply with your information above!**"

      else:
        message += "Thank you for your interest!"
        if product_names:
            message += f" You asked about: {product_names}."

      return message


    
    @staticmethod
    def extract_product_names_from_question(question: str) -> List[str]:
        """
        Extract potential product names from the user's question
        """
        # This is a simple extraction — can be improved by comparing with product database
        words = question.split()
        potential_products = []
        
        for word in words:
            if word[0].isupper() and len(word) > 2:
                potential_products.append(word)
        
        return potential_products

    @staticmethod
    def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
      """
        Extract email and phone number from the user message.
     """
      email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
      phone_match = re.search(r'\b(?:\+212|0)[5-7]\d{8}\b', text)

      return {
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None
    }
