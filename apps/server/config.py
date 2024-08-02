import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "postgres")
DATABASE_URL = f"postgresql+asyncpg://postgres:{DATABASE_PASSWORD}@db/db" 
