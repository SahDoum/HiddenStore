import asyncio

from init import dp, bot, redis_client
from handlers.notifiers import register_notifiers
import handlers.commands
import handlers.callbacks


async def main():
    await register_notifiers()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
