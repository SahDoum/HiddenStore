# import pydantic.json
# import json

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import pydantic.json
import json

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db/db"  # os.environ.get("DATABASE_URL")


# def _custom_json_serializer(*args, **kwargs) -> str:
#     """
#     Encodes json in the same way that pydantic does.
#     """
#     return json.dumps(*args, default=pydantic.json.pydantic_encoder, **kwargs)


engine = create_async_engine(DATABASE_URL, echo=True, future=True) # , json_serializer=_custom_json_serializer)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        return session
