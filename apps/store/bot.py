import asyncio

from init import dp, bot
from handlers.notifiers import register_notifiers
import handlers.orders
import handlers.items
import handlers.pickuploints
import handlers.helper


async def main():
    await register_notifiers()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
