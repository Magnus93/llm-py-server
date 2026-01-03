from dotenv import load_dotenv
import os

load_dotenv()  # only here once

OLLAMA_BASE_URL = os.environ["OLLAMA_BASE_URL"]
BRAVE_BASE_URL = os.environ.get("BRAVE_BASE_URL")
BRAVE_API_KEY = os.environ.get("BRAVE_API_KEY")