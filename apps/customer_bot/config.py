import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
SERVER_URL = os.getenv("SERVER_URL", "http://server:8000")
WEBAPP_URL = "https://" + str(os.getenv("DOMAIN_URL"))
