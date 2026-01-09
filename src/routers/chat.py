from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Literal, Union, List
from src.core import config
from src.services.brave_search import brave_search
import requests
import json


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information, recent events or facts that may have changed",
            "parameters": {
                "type": "object",
                "required": ["query"],
                "properties": {
                    "query": {"type": "string","description": "The search query"}
                }
            }
        }
    }
]
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

class ToolCall(Exception):
    def __init__(self, call):
        print("ToolCall", f"{call}")
        self.call = call


def stream_ollama(payload):
    with requests.post(
        f"{config.OLLAMA_BASE_URL}/api/chat",
        json=payload,
        stream=True
    ) as r:
        buffer = ""
        for line in r.iter_lines():
            if not line:
                continue

            chunk = line.decode("utf-8")
            buffer += chunk

            try:
                data = json.loads(buffer)
                buffer = ""
                tool_calls = data.get("message", {}).get("tool_calls")

                if tool_calls:
                    raise ToolCall(tool_calls[0])
                    
                yield chunk.encode("utf-8") + b"\n"
                buffer = ""

            except json.JSONDecodeError:
                # Partial JSON, keep buffering
                continue


router = APIRouter(prefix="/api")

@router.post("/chat")
async def chat(req: ChatRequest): 
    print("user_message", req.messages[len(req.messages) - 1].content)
    payload = req.model_dump()
    payload["tools"] = TOOLS

    print("payload:\n", payload)

    def generator():
        try:
            yield from stream_ollama(payload)

        except ToolCall as tc:
            query = tc.call["function"]["arguments"]["query"]
            tool_id = tc.call["id"]

            print("brave_search with query:", "f{query}")
            results = brave_search(query)

            payload["messages"].append({
                "role": "tool",
                "tool_call_id": tool_id,
                "content": json.dumps(results)
            })

            yield from stream_ollama(payload)

    return StreamingResponse(
        generator(),
        media_type="application/json"
    )
