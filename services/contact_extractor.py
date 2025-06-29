import re
from typing import Dict, Optional
from services.ai_services import AiService

class ContactExtractor:
    """
    Service to extract contact information from user responses
    """
    
    @staticmethod
    def extract_contact_info(user_message: str) -> Dict:
        """
        Extract contact information from user message using regex patterns
        """
        contact_info = {}
        
        # Extract phone number (various formats)
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # 123-456-7890 or 123.456.7890 or 1234567890
            r'\(\d{3}\)\s?\d{3}[-.]?\d{4}',    # (123) 456-7890
            r'\+1\s?\d{3}[-.]?\d{3}[-.]?\d{4}', # +1 123-456-7890
            r'\+?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}',  # International
            r'[0-9]{10,15}',  # Simple number
            r'\+?[0-9]{2,4}\s*[0-9]{2,4}\s*[0-9]{2,4}\s*[0-9]{2,4}',  # International with spaces
            r'\+33\s*[0-9]{1,2}\s*[0-9]{2}\s*[0-9]{2}\s*[0-9]{2}\s*[0-9]{2}',  # French format
            r'0[1-9]\s*[0-9]{2}\s*[0-9]{2}\s*[0-9]{2}\s*[0-9]{2}'  # French mobile
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, user_message)
            if phone_match:
                contact_info['phone'] = phone_match.group()
                break
        
        # Extract age (simple number between 16-99)
        age_match = re.search(r'\b(1[6-9]|[2-9]\d)\b', user_message)
        if age_match:
            potential_age = int(age_match.group())
            if 16 <= potential_age <= 99:
                contact_info['age'] = potential_age
        
        # Extract name (look for patterns like "je m'appelle", "mon nom est", etc.)
        name_patterns = [
            # French patterns
            r"je m'appelle\s+([a-zA-ZÀ-ÿ\s]+)",
            r"mon nom est\s+([a-zA-ZÀ-ÿ\s]+)",
            r"nom\s*:\s*([a-zA-ZÀ-ÿ\s]+)",
            r"je suis\s+([a-zA-ZÀ-ÿ\s]+)",
            r"appelle\s+([a-zA-ZÀ-ÿ\s]+)",
            r"nom\s+([a-zA-ZÀ-ÿ\s]+)",
            r"prénom\s+([a-zA-ZÀ-ÿ\s]+)",
            r"prénom\s*:\s*([a-zA-ZÀ-ÿ\s]+)",
            # English patterns
            r"name\s*:\s*([a-zA-ZÀ-ÿ\s]+)",
            r"i'm\s+([a-zA-ZÀ-ÿ\s]+)",
            r"my name is\s+([a-zA-ZÀ-ÿ\s]+)",
            r"i am\s+([a-zA-ZÀ-ÿ\s]+)",
            r"call me\s+([a-zA-ZÀ-ÿ\s]+)",
            r"my name's\s+([a-zA-ZÀ-ÿ\s]+)",
            r"i'm called\s+([a-zA-ZÀ-ÿ\s]+)",
            r"my name\s+([a-zA-ZÀ-ÿ\s]+)",
            r"first name\s*:\s*([a-zA-ZÀ-ÿ\s]+)",
            r"last name\s*:\s*([a-zA-ZÀ-ÿ\s]+)",
            r"full name\s*:\s*([a-zA-ZÀ-ÿ\s]+)",
            # More flexible patterns
            r"name\s+([a-zA-ZÀ-ÿ\s]+)",
            r"called\s+([a-zA-ZÀ-ÿ\s]+)",
            r"named\s+([a-zA-ZÀ-ÿ\s]+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, user_message.lower())
            if match:
                contact_info['name'] = match.group(1).strip().title()
                break
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, user_message)
        if email_match:
            contact_info['email'] = email_match.group(0)
        
        # Determine confidence level
        confidence = "low"
        if contact_info.get('name') and contact_info.get('email') and contact_info.get('phone'):
            confidence = "high"
        elif (contact_info.get('name') and contact_info.get('email')) or (contact_info.get('name') and contact_info.get('phone')) or (contact_info.get('email') and contact_info.get('phone')):
            confidence = "medium"
        
        contact_info['confidence'] = confidence
        contact_info['extraction_method'] = 'regex'
        
        return contact_info
    
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
            # French keywords
            "nom", "name", "email", "mail", "téléphone", "phone", "tél", "tel",
            "je m'appelle", "mon nom est", "prénom", "appelle",
            # English keywords
            "my name is", "i'm", "i am", "call me", "my name's", "i'm called",
            "first name", "last name", "full name", "contact", "contact info",
            "phone number", "mobile", "cell", "cell phone", "telephone",
            "email address", "e-mail", "mail address",
            # Common symbols
            "@", ".com", ".fr", ".net", ".org", ".co.uk", ".ca"
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