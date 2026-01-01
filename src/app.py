from fastapi import FastAPI
from fastapi.responses import StreamingResponse
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

@app.get("/chat")
def list_chat():
    return conversation

@app.post("/chat")
def chat(req: ChatRequest): 
    print("user_message", req)
    conversation.append({"role": "user", "content": req.user_message})

    payload = {
        "model": MODEL,
        "messages": conversation,
        "stream": True
    }

    return StreamingResponse(
        stream_ollama(payload),
        media_type="application/json"
    )


def stream_ollama(payload):
    with requests.post(
        f"{OLLAMA_URL}/api/chat",
        json=payload,
        stream=True
    ) as r:
        for line in r.iter_lines():
            if line:
                yield line + b"\n"