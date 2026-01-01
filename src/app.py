from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import Literal, Union, List
import requests

app = FastAPI()


OLLAMA_URL = "http://127.0.0.1:11434"
MODEL = "mistral"


@app.get("")
def is_alive():
    return "Yep, py server is running :)"

class ContentParts(BaseModel):
    text: str
    type: str

class MessageRequest(BaseModel):
    content: Union[str, List[ContentParts]]
    role: Literal["developer", "user", "assistant"]

# https://platform.openai.com/docs/api-reference/chat/create
class ChatCompletionsRequest(BaseModel):
    model: str
    messages: List[MessageRequest]


def stream_ollama(payload):
    with requests.post(
        f"{OLLAMA_URL}/api/chat",
        json=payload,
        stream=True
    ) as r:
        for line in r.iter_lines():
            if line:
                yield line + b"\n"

@app.post("/api/chat")
async def chat(req: ChatCompletionsRequest): 
    print("user_message", req.messages[len(req.messages) - 1].content)
    payload = req.model_dump()

    return StreamingResponse(
        stream_ollama(payload),
        media_type="application/json"
    )



@app.get("/v1/models")
def list_models():
    ollama_models = requests.get(f"{OLLAMA_URL}/api/tags").json()
    return {
        "object": "list",
        "data": [
            {
                "id": m["name"].split(":")[0], # Just "mistral", no version
                "object": "model",
                "owned_by": "local"
            }
            for m in ollama_models
        ]
    }

@app.get("/api/tags")
def proxy_tags():
    r = requests.get(f"{OLLAMA_URL}/api/tags")
    return JSONResponse(content=r.json())


@app.get("/api/version")
def proxy_version():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/version")
        return JSONResponse(content=r.json())
    except:
        return {"version": "unknown"}
    

@app.get("/api/ps")
def proxy_ps():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/ps")
        return JSONResponse(content=r.json())
    except:
        return {"status": "ok"}