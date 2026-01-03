
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
from src.core import config

router = APIRouter()

class WebSearchRequest(BaseModel):
    query: str


@router.post("/brave/search")
def brave_search(req: WebSearchRequest):
    url = f"{config.BRAVE_BASE_URL}/res/v1/web/search"
    params = { "q": req.query }
    headers = {
        "X-Subscription-Token": config.BRAVE_API_KEY
    }
    try:
        r = requests.get(url, params=params, headers=headers)
        return JSONResponse(content=r.json())
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
    except requests.exceptions.Timeout as e:
        print("Request timed out:", e)
    except requests.exceptions.RequestException as e:
        print("Other error:", e)