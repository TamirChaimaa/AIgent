# 💻 SmartByte AI Agent

A smart ecommerce platform featuring , an AI-powered shopping assistant that helps users find the ideal **laptop** through natural conversation. Built using modern web technologies, SmartByte delivers a seamless and intuitive shopping experience.

## 🌐 Live Demo

👉 [**Explore SmartByte AI Agent**](https://frontend-ai-agent.vercel.app/)

## 🖼️ Project Preview

<table>
  <tr>
    <td width="50%">
      <p style="text-align:center"><em>Welcome Screen - Meet Amine</em></p>
      <img src="https://github.com/TamirChaimaa/FrontendAIAgent/blob/main/public/smartbyte.png" alt="Welcome Screen - Meet Amine" style="width:100%">
    </td>
    <td width="50%">
      <p style="text-align:center"><em>AI-Powered Search Results</em></p>
      <img src="https://github.com/TamirChaimaa/FrontendAIAgent/blob/main/public/smartbyte1.png" alt="AI-Powered Search Results" style="width:100%">
    </td>
      <td width="50%">
      <p style="text-align:center"><em>AI-Powered Search Results</em></p>
      <img src="https://github.com/TamirChaimaa/FrontendAIAgent/blob/main/public/smartbyte2.png" alt="AI-Powered Search Results" style="width:100%">
    </td>
  </tr>
</table>

## 🚀 Features

### 🤖 AI Assistant 

* Conversational Search
* Intelligent Filtering
* Real-Time Inventory Check
* Customer Interest Logging

### 💼 Product Catalog

* Top Brands: Apple, Dell, Lenovo, HP, Asus
* Use Cases: Programming, Gaming, Business, Student
* Filter by: RAM, processor, storage, screen size, battery

### 💬 Chat Experience

* Seamless Conversations
* Visual Laptop Displays
* Quick Reservations
* Responsive Design

---

## 🛠️ Tech Stack

This project follows the **Model-View-Controller (MVC)** architectural pattern to ensure a clean separation of concerns, making it easier to maintain, scale, and test.

**Frontend**
React, Tailwind CSS, Vite

**Backend**
Flask (Python), Gemini Flash 1.5 (LLM), MongoDB

**Deployment**
Frontend: Vercel
Backend: Railway
Database: MongoDB Atlas

---

## ⚙️ How It Works

1. User Chat → 2. AI Understanding → 3. Product Matching → 4. Result Display → 5. Lead Capture → 6. Follow-up Ready

---

## 📦 MongoDB Schema

### messages Collection

```json
{
  "_id": "68610fb664e52aedfb5c9f95",
  "product_ids": ["product_id_1", "product_id_2"],
  "question": "What are the prices of products X and Y?",
  "answer": "Product X is €45, Product Y is €60.",
  "timestamp": "2025-06-22T09:10:00Z"
}
```

### leads Collection

```json
{
  "_id": "6861a507631e5d8fdcd8cb76",
  "name": "To be provided",
  "email": "pending@example.com",
  "phone": "To be provided",
  "interested_products": ["product_id"],
  "source_message_id": "6861a505631e5d8fdcd8cb75",
  "status": "new",
  "created_at": "2025-06-29T20:41:43.617Z",
  "last_contact": "2025-06-29T20:41:43.617Z",
  "notes": ""
}
```

### products Collection

```json
{
  "_id": "6860899164e52aedfb5c9f8f",
  "name": "MacBook Air M2",
  "description": "Lightweight laptop with the M2 chip, ideal for coding and productivity",
  "price": 999,
  "tags": ["laptop", "programming", "portable"],
  "image_url": "https://...",
  "specs": {
    "processor": "Apple M2",
    "ram": "8GB",
    "storage": "256GB SSD",
    "screen_size": "13.6 inch",
    "battery_life": "18 hours",
    "weight": "1.24 kg",
    "os": "macOS Ventura",
    "ports": ["2x Thunderbolt 4", "MagSafe 3", "3.5mm audio jack"],
    "keyboard": "Magic Keyboard with Touch ID"
  },
  "warranty": "1 year",
  "brand": "Apple",
  "release_date": "2022-07-01",
  "rating": 4.8,
  "reviews_count": 354,
  "available": true,
  "category": "Laptops",
  "created_at": "2025-06-29T00:00:00Z"
}
```

---

## 🧪 Test Scenarios

* "I need a MacBook for programming"
* "What’s the price of Dell laptops under \$1000?"
* "Can I reserve the Lenovo gaming model?"

---

## 🧰 Installation

### Frontend

```bash
cd frontendaiagent
npm start
```

### Backend

```bash
cd aigent
pip install -r requirements.txt
python server.py
```

---

## 🙏 Acknowledgments

* Gemini Flash 1.5
* MongoDB Atlas
* Vercel & Railway
* Open-source community

---

## 🔮 Future Enhancements

* Voice Search
* Image-based Search
* Payment Integration
* French & Arabic Support
* Inventory Management for Admins


## 📝 License

This project is for educational use only. All rights reserved.
