from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()


OLLAMA_URL = "http://127.0.0.1:11434"
MODEL = "mistral"

conversation = [
    { "role": "system", "content": "You are a helpful assistant. Be short and concise." } 
]


class ChatRequest(BaseModel):
    user_message: str


@app.post("/chat")
def chat(req: ChatRequest): 
    print("user_message", req)
    conversation.append({"role": "user", "content": req.user_message})

    payload = {
        "model": MODEL,
        "messages": conversation,
        "stream": False
    }

    r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload)
    print("r.text:", r.text)
    data = r.json()
    print(data)

    assistant_msg = data["message"]
    conversation.append(assistant_msg)

    return assistant_msg


@app.get("/chat")
def list_chat():
    return conversation