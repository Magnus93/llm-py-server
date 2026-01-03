
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def is_alive():
    return "Yep, py server is running - YAAAAAY!"