from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
from src.core import config

def brave_search(query: str) -> List[dict]:
    url = f"{config.BRAVE_BASE_URL}/res/v1/web/search"
    params = { "q": query }
    headers = {
        "X-Subscription-Token": config.BRAVE_API_KEY
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        res_body = response.json()
        results = res_body.get("web", {}).get("results", [])
        results2 = [
            {
                "title": result["title"], 
                "description": result["description"]
            }
            for result in results    
        ]
        print("results2", results2)
        return results2


    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
    except requests.exceptions.Timeout as e:
        print("Request timed out:", e)
    except requests.exceptions.RequestException as e:
        print("Other error:", e)