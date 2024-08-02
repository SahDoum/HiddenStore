import os

SERVER_URL = os.getenv("SERVER_URL", "http://server:8000")
TOKEN = os.getenv("TELEGRAM_TOKEN") or ""
