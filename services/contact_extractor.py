import re
from typing import Dict, Optional
from services.ai_services import AiService

class ContactExtractor:
    """
    Service to extract contact information from user responses
    """
    
    @staticmethod
    def extract_contact_info(user_response: str) -> Dict:
        """
        Extract contact information from user response using AI
        """
        try:
            # Use AI to extract contact information
            ai_service = AiService()
            
            prompt = f"""
            Extract contact information from this user response. Return ONLY a JSON object with the following structure:
            
            User Response: "{user_response}"
            
            Expected JSON format:
            {{
                "name": "extracted name or null",
                "email": "extracted email or null", 
                "phone": "extracted phone or null",
                "confidence": "high/medium/low",
                "extraction_method": "ai/regex/combined"
            }}
            
            Rules:
            1. Extract name, email, and phone if present
            2. If not found, use null
            3. For confidence: high (clear info), medium (partial), low (unclear)
            4. For extraction_method: ai (AI extracted), regex (pattern matched), combined (both)
            
            Return ONLY the JSON object, nothing else.
            """
            
            response = ai_service.ask_question(prompt)
            
            if isinstance(response, dict) and 'message' in response:
                response_text = response['message']
                
                # Try to extract JSON from AI response
                if "{" in response_text and "}" in response_text:
                    json_start = response_text.find("{")
                    json_end = response_text.rfind("}") + 1
                    json_str = response_text[json_start:json_end]
                    
                    import json
                    contact_data = json.loads(json_str)
                    
                    # Validate extracted data
                    contact_data = ContactExtractor._validate_extracted_data(contact_data)
                    
                    return contact_data
                else:
                    # Fallback to regex extraction
                    return ContactExtractor._extract_with_regex(user_response)
            else:
                # Fallback to regex extraction
                return ContactExtractor._extract_with_regex(user_response)
                
        except Exception as e:
            print(f"Error extracting contact info with AI: {e}")
            # Fallback to regex extraction
            return ContactExtractor._extract_with_regex(user_response)
    
    @staticmethod
    def _extract_with_regex(user_response: str) -> Dict:
        """
        Extract contact information using regex patterns
        """
        response_lower = user_response.lower()
        
        # Extract name (look for patterns like "je m'appelle", "mon nom est", etc.)
        name = None
        name_patterns = [
            r"je m'appelle\s+([a-zA-ZÀ-ÿ\s]+)",
            r"mon nom est\s+([a-zA-ZÀ-ÿ\s]+)",
            r"nom\s*:\s*([a-zA-ZÀ-ÿ\s]+)",
            r"name\s*:\s*([a-zA-ZÀ-ÿ\s]+)",
            r"je suis\s+([a-zA-ZÀ-ÿ\s]+)",
            r"i'm\s+([a-zA-ZÀ-ÿ\s]+)",
            r"my name is\s+([a-zA-ZÀ-ÿ\s]+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, response_lower)
            if match:
                name = match.group(1).strip().title()
                break
        
        # Extract email
        email = None
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, user_response)
        if email_match:
            email = email_match.group(0)
        
        # Extract phone
        phone = None
        phone_patterns = [
            r'\+?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}',
            r'[0-9]{10,15}',
            r'\+?[0-9]{2,4}\s*[0-9]{2,4}\s*[0-9]{2,4}\s*[0-9]{2,4}'
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, user_response)
            if phone_match:
                phone = phone_match.group(0)
                break
        
        # Determine confidence level
        confidence = "low"
        if name and email and phone:
            confidence = "high"
        elif (name and email) or (name and phone) or (email and phone):
            confidence = "medium"
        
        return {
            "name": name,
            "email": email,
            "phone": phone,
            "confidence": confidence,
            "extraction_method": "regex"
        }
    
    @staticmethod
    def _validate_extracted_data(contact_data: Dict) -> Dict:
        """
        Validate and clean extracted contact data
        """
        # Validate email format
        if contact_data.get("email"):
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not re.match(email_pattern, contact_data["email"]):
                contact_data["email"] = None
        
        # Validate phone format (basic validation)
        if contact_data.get("phone"):
            # Remove non-digit characters except + for international format
            phone_clean = re.sub(r'[^\d+]', '', contact_data["phone"])
            if len(phone_clean) < 8:  # Too short for a phone number
                contact_data["phone"] = None
            else:
                contact_data["phone"] = phone_clean
        
        # Clean name
        if contact_data.get("name"):
            # Remove extra spaces and capitalize properly
            name_clean = " ".join(contact_data["name"].split()).title()
            contact_data["name"] = name_clean
        
        return contact_data
    
    @staticmethod
    def is_contact_info_response(user_response: str) -> bool:
        """
        Check if user response contains contact information
        """
        response_lower = user_response.lower()
        
        # Keywords that indicate contact information
        contact_keywords = [
            "nom", "name", "email", "mail", "téléphone", "phone", "tél", "tel",
            "je m'appelle", "mon nom est", "my name is", "i'm",
            "@", ".com", ".fr", ".net", ".org"
        ]
        
        # Check for email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        has_email = bool(re.search(email_pattern, user_response))
        
        # Check for phone pattern
        phone_pattern = r'\+?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}'
        has_phone = bool(re.search(phone_pattern, user_response))
        
        # Check for contact keywords
        has_keywords = any(keyword in response_lower for keyword in contact_keywords)
        
        return has_email or has_phone or has_keywords
    
    @staticmethod
    def generate_follow_up_message(extracted_data: Dict) -> str:
        """
        Generate a follow-up message based on extracted contact information
        """
        missing_fields = []
        
        if not extracted_data.get("name"):
            missing_fields.append("nom")
        if not extracted_data.get("email"):
            missing_fields.append("email")
        if not extracted_data.get("phone"):
            missing_fields.append("téléphone")
        
        if not missing_fields:
            return "✅ Parfait ! J'ai bien reçu vos informations. Je vais vous contacter très prochainement pour un suivi personnalisé !"
        
        if len(missing_fields) == 1:
            return f"Merci ! Il me manque juste votre {missing_fields[0]}. Pouvez-vous me le fournir ?"
        else:
            missing_text = ", ".join(missing_fields[:-1]) + f" et {missing_fields[-1]}"
            return f"Merci ! Il me manque encore votre {missing_text}. Pouvez-vous me les fournir ?" 