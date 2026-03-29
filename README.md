# 🎯 AI Interview Backend

A REST API that runs AI-powered mock interviews. Pick a role, answer 5 questions one by one, and get feedback after each answer plus a final score out of 10. Supports Python Developer, Java Developer, and AI Engineer tracks — powered by LLaMA 3.3 70B via Groq.

---

## ⚡ Tech Stack

| | |
|---|---|
| **Framework** | FastAPI |
| **AI Model** | LLaMA 3.3 70B via Groq API |
| **Language** | Python |
| **Memory** | In-memory per session |

---

## 🎭 Interview Tracks

| Role | Topics Covered |
|---|---|
| `ai_engineer` | ML, deep learning, neural networks, TensorFlow, PyTorch, AI system design |
| `java_developer` | Java, OOP, Spring Boot, REST APIs, databases, system design |
| `python_developer` | Python concepts, OOP, APIs, data structures, best practices |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/parkash34/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment
```bash
cp .env.example .env
```
Then open `.env` and add your Groq API key:
```
API_KEY=your_groq_api_key_here
```

### 4. Run the server
```bash
uvicorn main:app --reload
```

Server runs at `http://localhost:8000`

---

## 📡 API Usage

### `POST /start-interview`
Start a new interview session.

**Request body:**
```json
{
  "session_id": "user_123",
  "name": "Om",
  "role": "python_developer"
}
```

**Response:**
```json
{
  "message": "Hi Om! Let's start. What is the difference between a list and a tuple in Python?"
}
```

---

### `POST /answer`
Submit your answer and get feedback + next question.

**Request body:**
```json
{
  "session_id": "user_123",
  "answer": "A list is mutable while a tuple is immutable..."
}
```

**Response:**
```json
{
  "message": "Good answer! You covered the key difference. One thing to add is that tuples are generally faster... Next question: Explain Python's GIL."
}
```

> After 5 questions the interviewer gives an overall score out of 10 and a summary.

---

## 📁 Project Structure

```
ai-interview-backend/
├── main.py            # FastAPI app, routes, and AI logic
├── requirements.txt   # Python dependencies
├── .env               # Your API key (never commit this)
├── .env.example       # Template for environment variables
├── .gitignore         # Ignores .env and pycache
└── README.md
```

---

## ⚠️ Important

Make sure `.gitignore` includes:
```
.env
__pycache__/
```

Never push your API key to GitHub.

---

## 👤 Author

**Ohm Parkash** — [LinkedIn](https://www.linkedin.com/in/om-parkash34/) · [GitHub](https://github.com/parkash34)
