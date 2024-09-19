import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
KITCHEN_TG_ID = os.getenv("KITCHEN_TG_ID")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
SERVER_URL = os.getenv("SERVER_URL", "http://server:8000")

ORDERS_PER_PAGE = 3

admins_str = os.getenv("ADMINS", "")
ADMINS = [int(admin_id) for admin_id in admins_str.split(",") if admin_id]
