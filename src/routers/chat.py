from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Literal, Union, List
from src.core import config
import requests


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
        f"{config.OLLAMA_BASE_URL}/api/chat",
        json=payload,
        stream=True
    ) as r:
        for line in r.iter_lines():
            if line:
                yield line + b"\n"


router = APIRouter(prefix="/api")

@router.post("/chat")
async def chat(req: ChatCompletionsRequest): 
    print("user_message", req.messages[len(req.messages) - 1].content)
    payload = req.model_dump()

    return StreamingResponse(
        stream_ollama(payload),
        media_type="application/json"
    )
