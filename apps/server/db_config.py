# import os
import pydantic.json
import json

# from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db/db"  # os.environ.get("DATABASE_URL")


def _custom_json_serializer(*args, **kwargs) -> str:
    """
    Encodes json in the same way that pydantic does.
    """
    return json.dumps(*args, default=pydantic.json.pydantic_encoder, **kwargs)


engine = create_async_engine(DATABASE_URL, echo=True)#, future=True, json_serializer=_custom_json_serializer)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# async def init_db():
#     async with engine.begin() as conn:
#         # await conn.run_sync(SQLModel.metadata.drop_all)
#         await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        return session
