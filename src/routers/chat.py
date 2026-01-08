from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Literal, Union, List
from src.core import config
from src.services import brave_search
import requests
import json


system_message = {
    "role": "system",
    "content": '''
You have access to a web search tool.
If you need information from the web, respond ONLY in JSON format like: 
{"action": "search", "query": "<what to search>"}
Do NOT output any other text outside this JSON.
'''
}

class ContentParts(BaseModel):
    text: str
    type: str

class MessageRequest(BaseModel):
    content: Union[str, List[ContentParts]]
    role: Literal["system", "developer", "user", "assistant"]

# https://platform.openai.com/docs/api-reference/chat/create
class ChatRequest(BaseModel):
    model: str
    messages: List[MessageRequest]



def stream_ollama(payload):
    with requests.post(
        f"{config.OLLAMA_BASE_URL}/api/chat",
        json=payload,
        stream=True
    ) as r:
        buffer = ""
        for line in r.iter_lines():
            print("line:\t", line)
            if line:
                chunk = line.decode("utf-8")
                buffer += chunk

                try:
                    data = json.loads(buffer)
                    if  "action" in data and data["action"] == "search":
                        query = data["query"]
                        search_results = brave_search(query)
                        yield ({"tool": "search", "query": query, "results": search_results}).encode("utf-8") + "b\n"
                        buffer=""
                    else:
                        yield chunk.encode("utf-8") + b"\n"
                        buffer = ""
                except json.JSONDecodeError:
                    yield chunk.encode("utf-8") + b"\n"


router = APIRouter(prefix="/api")

@router.post("/chat")
async def chat(req: ChatRequest): 
    print("user_message", req.messages[len(req.messages) - 1].content)
    payload = req.model_dump()
    payload["messages"].append(system_message)

    print("payload:\n", payload)

    return StreamingResponse(
        stream_ollama(payload),
        media_type="application/json"
    )
