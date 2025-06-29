from datetime import datetime
from config.db import db

class LeadModel:
    @staticmethod
    def create_lead(name, email, phone, interested_products, source_message_id=None):
        """
        Create a new lead record
        """
        try:
            lead_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "interested_products": interested_products,
                "source_message_id": source_message_id,
                "status": "new",  # new, contacted, converted, lost
                "created_at": datetime.utcnow().isoformat() + "Z",
                "last_contact": datetime.utcnow().isoformat() + "Z",
                "notes": ""
            }
            
            result = db.leads.insert_one(lead_data)
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"Error creating lead: {e}")
            return None
    
    @staticmethod
    def get_all_leads():
        """
        Get all leads
        """
        try:
            leads = list(db.leads.find().sort("created_at", -1))
            for lead in leads:
                lead["_id"] = str(lead["_id"])
            return leads
        except Exception as e:
            print(f"Error getting leads: {e}")
            return []
    
    @staticmethod
    def get_lead_by_email(email):
        """
        Get lead by email
        """
        try:
            lead = db.leads.find_one({"email": email})
            if lead:
                lead["_id"] = str(lead["_id"])
            return lead
        except Exception as e:
            print(f"Error getting lead by email: {e}")
            return None
    
    @staticmethod
    def update_lead_status(lead_id, status, notes=""):
        """
        Update lead status
        """
        try:
            from bson import ObjectId
            update_data = {
                "status": status,
                "last_contact": datetime.utcnow().isoformat() + "Z"
            }
            if notes:
                update_data["notes"] = notes
                
            result = db.leads.update_one(
                {"_id": ObjectId(lead_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating lead status: {e}")
            return False
    
    @staticmethod
    def get_leads_by_status(status):
        """
        Get leads by status
        """
        try:
            leads = list(db.leads.find({"status": status}).sort("created_at", -1))
            for lead in leads:
                lead["_id"] = str(lead["_id"])
            return leads
        except Exception as e:
            print(f"Error getting leads by status: {e}")
            return []
    
    @staticmethod
    def delete_lead(lead_id):
        """
        Delete a lead
        """
        try:
            from bson import ObjectId
            result = db.leads.delete_one({"_id": ObjectId(lead_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting lead: {e}")
            return False
    
    @staticmethod
    def get_lead_with_messages(lead_id):
        """
        Get lead with all related messages
        """
        try:
            from bson import ObjectId
            lead = db.leads.find_one({"_id": ObjectId(lead_id)})
            if not lead:
                return None
            
            lead["_id"] = str(lead["_id"])
            
            # Get the source message
            if lead.get("source_message_id"):
                source_message = db.messages.find_one({"_id": ObjectId(lead["source_message_id"])})
                if source_message:
                    source_message["_id"] = str(source_message["_id"])
                    lead["source_message"] = source_message
            
            # Get all messages related to this lead (by email or phone)
            related_messages = []
            if lead.get("email") and lead["email"] != "pending@example.com":
                # Find messages that might be from the same person
                # This is a simple approach - you could make it more sophisticated
                related_messages = list(db.messages.find({
                    "$or": [
                        {"question": {"$regex": lead["email"], "$options": "i"}},
                        {"answer": {"$regex": lead["email"], "$options": "i"}}
                    ]
                }).sort("timestamp", -1))
            
            # Convert ObjectIds to strings
            for message in related_messages:
                message["_id"] = str(message["_id"])
            
            lead["related_messages"] = related_messages
            lead["total_messages"] = len(related_messages)
            
            return lead
            
        except Exception as e:
            print(f"Error getting lead with messages: {e}")
            return None
    
    @staticmethod
    def get_leads_by_message_id(message_id):
        """
        Get all leads that originated from a specific message
        """
        try:
            from bson import ObjectId
            leads = list(db.leads.find({"source_message_id": message_id}).sort("created_at", -1))
            for lead in leads:
                lead["_id"] = str(lead["_id"])
            return leads
        except Exception as e:
            print(f"Error getting leads by message ID: {e}")
            return []
    
    @staticmethod
    def get_conversation_history(lead_id):
        """
        Get complete conversation history for a lead
        """
        try:
            from bson import ObjectId
            lead = db.leads.find_one({"_id": ObjectId(lead_id)})
            if not lead:
                return None
            
            lead["_id"] = str(lead["_id"])
            
            # Get all messages in chronological order
            all_messages = list(db.messages.find().sort("timestamp", 1))
            
            # Convert ObjectIds to strings
            for message in all_messages:
                message["_id"] = str(message["_id"])
            
            # Create conversation timeline
            conversation = {
                "lead": lead,
                "messages": all_messages,
                "total_messages": len(all_messages),
                "conversation_start": all_messages[0]["timestamp"] if all_messages else None,
                "conversation_end": all_messages[-1]["timestamp"] if all_messages else None
            }
            
            return conversation
            
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return None
    
    @staticmethod
    def link_message_to_lead(lead_id, message_id):
        """
        Link a message to a lead (for additional messages after lead creation)
        """
        try:
            from bson import ObjectId
            update_data = {
                "linked_message_ids": [message_id],
                "last_contact": datetime.utcnow().isoformat() + "Z"
            }
            
            # Add to existing linked messages if any
            lead = db.leads.find_one({"_id": ObjectId(lead_id)})
            if lead and lead.get("linked_message_ids"):
                update_data["linked_message_ids"] = lead["linked_message_ids"] + [message_id]
            
            result = db.leads.update_one(
                {"_id": ObjectId(lead_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
            
        except Exception as e:
            print(f"Error linking message to lead: {e}")
            return False
    
    @staticmethod
    def get_lead_analytics(lead_id):
        """
        Get analytics for a lead (message count, interest level, etc.)
        """
        try:
            from bson import ObjectId
            lead = db.leads.find_one({"_id": ObjectId(lead_id)})
            if not lead:
                return None
            
            lead["_id"] = str(lead["_id"])
            
            # Get all related messages
            related_messages = []
            if lead.get("source_message_id"):
                source_message = db.messages.find_one({"_id": ObjectId(lead["source_message_id"])})
                if source_message:
                    related_messages.append(source_message)
            
            if lead.get("linked_message_ids"):
                for msg_id in lead["linked_message_ids"]:
                    message = db.messages.find_one({"_id": ObjectId(msg_id)})
                    if message:
                        related_messages.append(message)
            
            # Calculate analytics
            analytics = {
                "lead_id": lead_id,
                "total_messages": len(related_messages),
                "first_message_date": related_messages[0]["timestamp"] if related_messages else None,
                "last_message_date": related_messages[-1]["timestamp"] if related_messages else None,
                "interested_products_count": len(lead.get("interested_products", [])),
                "lead_age_days": None,
                "conversion_probability": "medium"  # You could implement ML-based scoring here
            }
            
            # Calculate lead age
            if lead.get("created_at"):
                from datetime import datetime
                created_date = datetime.fromisoformat(lead["created_at"].replace("Z", "+00:00"))
                now = datetime.utcnow()
                analytics["lead_age_days"] = (now - created_date).days
            
            return analytics
            
        except Exception as e:
            print(f"Error getting lead analytics: {e}")
            return None 