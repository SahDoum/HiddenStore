from aiogram import types, BaseMiddleware
from config import ADMINS


class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, types.Message):
            user_id = event.from_user.id
            if user_id not in ADMINS:
                return
        return await handler(event, data)
