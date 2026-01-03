
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
from src.core import config

router = APIRouter(prefix="/api")

@router.get("/version")
def proxy_version():
    try:
        r = requests.get(f"{config.OLLAMA_BASE_URL}/api/version")
        return JSONResponse(content=r.json())
    except:
        return {"version": "unknown"}