# 🎓 AI Study Companion Chatbot

An intelligent terminal-based AI Study Companion built using Python and Gemini 2.5 Flash.

This chatbot helps students:

- Understand concepts clearly
- Prepare for exams
- Generate quizzes
- Create quick revision notes
- Track weak topics
- Improve study productivity

---

# 🚀 Features

✅ Explain concepts simply  
✅ Quiz generation mode  
✅ Exam preparation mode  
✅ Summary mode  
✅ Revision mode  
✅ Study timer  
✅ Persistent chat history  
✅ AI memory system  
✅ Weak topic detection  
✅ Favorite topic tracking  
✅ Clean terminal UI  
✅ Beginner-friendly

---

# 🛠 Tech Stack

- Python
- Gemini 2.5 Flash API
- google-generativeai
- dotenv
- colorama

---

# 📂 Project Structure

```bash
study_bot/
│
├── app.py
├── .env
├── requirements.txt
├── chat_history.json
├── memory.json
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/kumaratul1134/study-chatbot.git
```

## 2. Move Into Folder

```bash
cd study-bot
```

## 3. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Setup API Key

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Get Gemini API key from:

https://aistudio.google.com/app/apikey

---

# ▶️ Run The Bot

```bash
python app.py
```

---

# 💡 Available Commands

| Command    | Description           |
| ---------- | --------------------- |
| `/help`    | Show all commands     |
| `/mode`    | Show current mode     |
| `/explain` | Explanation mode      |
| `/quiz`    | Quiz mode             |
| `/summary` | Summary mode          |
| `/exam`    | Exam preparation mode |
| `/revise`  | Quick revision mode   |
| `/timer`   | Start study timer     |
| `/memory`  | Show AI memory        |
| `/clear`   | Clear memory/history  |
| `/exit`    | Exit chatbot          |

---

# 🧠 Modes

## Explain Mode

Explains concepts clearly with examples.

## Quiz Mode

Generates MCQs with answers.

## Summary Mode

Creates concise bullet-point summaries.

## Exam Mode

Provides exam-oriented preparation notes.

## Revision Mode

Creates ultra-short high-retention revision notes.

---

# 🧠 AI Memory System

The chatbot remembers:

- Favorite topics
- Weak topics
- Study sessions
- Last studied time

Memory is stored locally using JSON.

---

# ⏳ Study Timer

Built-in timer for focused study sessions.

Example:

```bash
/timer
```

---

# 🔥 Example Usage

```bash
/explain
dynamic programming
```

```bash
/exam
OSI Model
```

```bash
/revise
DBMS normalization
```

---

# 📌 Future Improvements

- GUI version
- Voice assistant
- PDF note upload
- Flashcards
- Personalized study planner
- Web version using Flask/React
- RAG-based memory

---

# 👨‍💻 Author : ATuL

Built with Python + Gemini Flash 🚀
