import React, { useState, useRef, useEffect } from "react";
import ChatHeader from "./ChatHeader";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";

const AIAssistant = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your AI assistant. How can I help you today?",
      sender: "ai",
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = useRef(null);

  // Store leadId if exists (state only)
  const [leadId, setLeadId] = useState(null);

  // Store lead name to know their name
  const [leadName, setLeadName] = useState("");

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (userMessage) => {
    if (!userMessage || userMessage.trim() === "") return;

    const baseId = Date.now();

    const newMessage = {
      id: baseId,
      text: userMessage,
      sender: "user",
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, newMessage]);

    const loadingMsg = {
      id: baseId + 1,
      text: "Thinking...",
      sender: "ai",
      isTyping: true,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, loadingMsg]);

    try {
      const BACKEND_URL = 'https://web-production-c9b7.up.railway.app/ai/ask';
      
      // Check if this message contains contact information
      const hasContactInfo = checkForContactInfo(userMessage);
      
      let requestBody = { question: userMessage };
      
      // If we have a leadId, include it in the request
      if (leadId) {
        requestBody.lead_id = leadId;
      }

      const response = await fetch(BACKEND_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });

      const data = await response.json();
      const aiResponse = data.answer || data.response || data.message || "";
      
      // Check if backend suggests lead capture
      const shouldShowLeadForm = data.should_capture_lead || false;

      setMessages(prev => {
        const updated = prev.filter(msg => !msg.isTyping);
        return [...updated, {
          id: baseId + 2,
          text: aiResponse || "Sorry, I couldn't process your request.",
          sender: 'ai',
          timestamp: new Date(),
          products: data.products || [],
          leadCaptureMessage: data.lead_capture_message || null,
          shouldCaptureLead: shouldShowLeadForm,
          preliminaryLeadId: data.preliminary_lead_id,
          linkedLeadId: data.linked_lead_id,
          contactExtraction: data.contact_extraction || null,
          leadUpdated: data.lead_updated || false,
          followUpMessage: data.follow_up_message || null
        }];
      });

      // If contact info was extracted and lead was updated, store the lead info
      if (data.contact_extraction && data.lead_updated) {
        const contactData = data.contact_extraction;
        if (contactData.name) {
          setLeadName(contactData.name);
        }
        if (data.linked_lead_id) {
          setLeadId(data.linked_lead_id);
        }
      }

    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => {
        const updated = prev.filter(msg => !msg.isTyping);
        return [...updated, {
          id: Date.now(),
          text: `Connection error: ${error.message}`,
          sender: 'ai',
          timestamp: new Date()
        }];
      });
    }
  };

  // Simple function to check if message contains contact information
  const checkForContactInfo = (message) => {
    const lowerMessage = message.toLowerCase();
    
    // Check for common contact patterns
    const hasName = /(je m'appelle|mon nom est|my name is|i'm|nom\s*:|name\s*:)/i.test(message);
    const hasEmail = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/.test(message);
    const hasPhone = /(\+?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}|[0-9]{10,15})/.test(message);
    
    return hasName || hasEmail || hasPhone;
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (inputValue.trim() !== "") {
        handleSendMessage(inputValue);
        setInputValue("");
      }
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <ChatHeader />
      <div className="flex-1 flex justify-center items-center">
        <div className="w-full max-w-xl h-[90vh] bg-white rounded-2xl shadow-xl flex flex-col p-2 sm:p-4 md:p-6 overflow-hidden">
          <div className="flex-1 overflow-y-auto space-y-4 px-1 sm:px-2 md:px-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === "ai" ? "justify-start" : "justify-end"}`}
              >
                <div className="w-full max-w-[80%]">
                  <ChatMessage message={message} />
                  
                  {/* Show lead capture message if needed */}
                  {message.sender === "ai" && message.shouldCaptureLead && (
                    <div className="mt-4 p-4 border border-blue-400 rounded-xl bg-blue-50 max-w-md mx-auto">
                      <h4 className="font-semibold mb-2 text-blue-700">
                        {message.leadCaptureMessage || "Please provide your contact information:"}
                      </h4>
                      <p className="text-sm text-blue-600">
                        Just reply with your name, email, and phone number in your next message.
                      </p>
                    </div>
                  )}
                  
                  {/* Show contact extraction results */}
                  {message.sender === "ai" && message.contactExtraction && (
                    <div className="mt-4 p-4 border border-green-400 rounded-xl bg-green-50 max-w-md mx-auto">
                      <h4 className="font-semibold mb-2 text-green-700">
                        ✅ Contact Information Received
                      </h4>
                      <div className="text-sm text-green-600 space-y-1">
                        {message.contactExtraction.name && (
                          <p><strong>Name:</strong> {message.contactExtraction.name}</p>
                        )}
                        {message.contactExtraction.email && (
                          <p><strong>Email:</strong> {message.contactExtraction.email}</p>
                        )}
                        {message.contactExtraction.phone && (
                          <p><strong>Phone:</strong> {message.contactExtraction.phone}</p>
                        )}
                        {message.contactExtraction.age && (
                          <p><strong>Age:</strong> {message.contactExtraction.age}</p>
                        )}
                        <p><strong>Confidence:</strong> {message.contactExtraction.confidence}</p>
                      </div>
                      {message.leadUpdated && (
                        <p className="mt-2 text-xs text-green-500">
                          ✅ Lead information updated successfully!
                        </p>
                      )}
                    </div>
                  )}
                  
                  {/* Show follow-up message if provided */}
                  {message.sender === "ai" && message.followUpMessage && (
                    <div className="mt-4 p-4 border border-yellow-400 rounded-xl bg-yellow-50 max-w-md mx-auto">
                      <h4 className="font-semibold mb-2 text-yellow-700">
                        📝 Additional Information Needed
                      </h4>
                      <p className="text-sm text-yellow-600">
                        {message.followUpMessage}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <ChatInput
            value={inputValue}
            onChange={setInputValue}
            onSend={handleSendMessage}
            onKeyPress={handleKeyPress}
          />
        </div>
      </div>
    </div>
  );
};

export default AIAssistant; 