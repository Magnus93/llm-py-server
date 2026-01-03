from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
from src.core import config


router = APIRouter(prefix="/api")


# Lists running models
@router.get("/ps")
def proxy_ps():
    try:
        r = requests.get(f"{config.OLLAMA_BASE_URL}/api/ps")
        return JSONResponse(content=r.json())
    except:
        return {"status": "ok"}