from aiogram.filters import Command
from init import dp


@dp.message(Command("help"))
async def cmd_delete_pickup_point(message):
    helper_message = """
        Команды:

        /pickuppoints
        /create_pickup_point

        /orders

        /items
        /create_item
    """

    await message.answer(helper_message)
