import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel


load_dotenv()

api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY is not set in the env.")

class StartInterview(BaseModel):
    session_id : str
    name : str
    role : str

class Answer(BaseModel):
    session_id : str
    answer : str

app = FastAPI()
memory = {}

system_prompts = {
    "ai_engineer": "You are a senior AI Engineer conducting a technical interview with {name}. Ask one question at a time about machine learning, deep learning, neural networks, AI frameworks like TensorFlow and PyTorch, and AI system design. After each answer give constructive feedback then ask the next question. After 5 questions give an overall score out of 10 and a summary. Ask only ONE question and then STOP. Wait for the candidate to answer before giving feedback or asking the next question. Do NOT answer your own questions or assume the candidate's response.",
    "java_developer": "You are a senior Java Developer conducting a technical interview with {name}. Ask one question at a time about Java, OOP principles, Spring Boot, REST APIs, databases, and system design. After each answer give constructive feedback then ask the next question. After 5 questions give an overall score out of 10 and a summary.Ask only ONE question and then STOP. Wait for the candidate to answer before giving feedback or asking the next question. Do NOT answer your own questions or assume the candidate's response.",
    "python_developer": "You are a senior Python Developer conducting a technical interview with {name}. Ask one question at a time about Python concepts, OOP, APIs, data structures, and best practices. After each answer give constructive feedback then ask the next question. After 5 questions give an overall score out of 10 and a summary.Ask only ONE question and then STOP. Wait for the candidate to answer before giving feedback or asking the next question. Do NOT answer your own questions or assume the candidate's response."
}

def ask_ai(chat_history):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "llama-3.3-70b-versatile",
                "temperature": 0.7,
                "max_tokens": 500,
                "messages": [
                    *chat_history
                ]
            },
            timeout=10
        )
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "Connection error. Please check your network."
    except requests.exceptions.HTTPError as e:
        return f"API error: {e.response.status_code}"
    except Exception as e:
        return f"Something went wrong: {str(e)}"
    
@app.post("/start-interview")
def start_interview(interview: StartInterview):
    if not interview.session_id.strip():
        return {"error": "Session ID is missing."}
    if not interview.name.strip():
        return {"error": "Name is missing."}
    if not interview.role.strip():
        return {"error": "Role is missing."}
    if interview.role not in ["python_developer", "ai_engineer", "java_developer"]:
        return {"error": "Invalid role. Please choose from python_developer, ai_engineer, or java_developer."}
    
    session_id = interview.session_id
    name = interview.name
    role = interview.role

    if session_id not in memory:
        memory[session_id] = []
    
    prompt = system_prompts[role].format(name=name)
    memory[session_id].append({"role": "system", "content": prompt})
    ai_reply = ask_ai(memory[session_id])

    memory[session_id].append({"role": "assistant", "content": ai_reply})
    return {"message": ai_reply}

@app.post("/answer")
def answer(answer: Answer):
    if not answer.session_id.strip():
        return {"error": "Session ID is missing."}
    if not answer.answer.strip():
        return {"error": "Please type an answer before sending."}
    
    session_id = answer.session_id
    user_answer = answer.answer

    if session_id not in memory:
        return {"error": "Session ID not found. Please start the interview first."}
    
    memory[session_id].append({"role": "user", "content": user_answer})
    ai_reply = ask_ai(memory[session_id])

    memory[session_id].append({"role": "assistant", "content": ai_reply})
    return {"message": ai_reply}