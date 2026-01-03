from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
from src.core import config


router = APIRouter(prefix="/api")

@router.get("/tags")
def proxy_tags():
    r = requests.get(f"{config.OLLAMA_BASE_URL}/api/tags")
    return JSONResponse(content=r.json())