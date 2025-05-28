# 📬 Telegram Goal & Reminder Chatbot

A Telegram-based chatbot that helps users **set goals**, **schedule reminders**, and **answer questions based on documents** ingested directly from Telegram. It leverages **FastAPI** for the backend, **RabbitMQ** for asynchronous task processing, and a modular chatbot architecture to support a variety of use cases.

---

## 🧠 Features

- ✅ Set personal and goal-oriented tasks via Telegram.
- ⏰ Receive reminders directly through the chat interface.
- 📄 Ingest and query documents sent via Telegram (e.g., PDFs, text files).
- 🤖 Acts as a general-purpose chatbot with conversational abilities.
- 🐇 Asynchronous processing using RabbitMQ for responsiveness and scalability.
- 📚 RAG-based document Q&A **(in process)**

---

## Installation

1. **Install python dependencies**
```bash
 pip install -r requirements.txt

```

2. **Set up your environment**
```bash
   Edit the provided .env files and add the appropriate configuration values (e.g., your Telegram bot token, RabbitMQ connection URL, etc.)
```

3. **Start rabbitmq**

```bash
 docker compose up
```

4. **Start the fastapi backend**
```bash
 cd backend
 python app.py
```

5. **Start the telegram server**
```bash
 cd telebot
 python main.py
```

✅ That’s it! Your Telegram chatbot is now running and ready to use.

### Demo
<iframe src="https://drive.google.com/file/d/1vU6IBA_HyyJB6-UrV8JPhjBYWORLb8Ah/preview?usp=drivesdk" 
 width="640" height="480" allow="autoplay"></iframe>