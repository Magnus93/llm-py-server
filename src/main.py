from fastapi import FastAPI
from src.routers import alive, tags, version, ps, chat, brave_search

app = FastAPI()

app.include_router(alive.router)
app.include_router(tags.router)
app.include_router(version.router)
app.include_router(ps.router)
app.include_router(chat.router)
app.include_router(brave_search.router)


