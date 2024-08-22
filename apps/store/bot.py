import asyncio

from init import dp, bot
from handlers.notifiers import register_notifiers
import handlers.callbacks
import handlers.commands

from object_create_fabric import ObjectCreateFabric
from libs.hidden_client import HiddenPickupPoint, HiddenItem

pickup_point_factory = ObjectCreateFabric(
    HiddenPickupPoint,
    fields={
        "address": "Введите адрес пункта самовывоза:",
        "description": "Введите описание пункта самовывоза:",
    },
    command_name="create_pickup_point",
    dp=dp,
)

menu_item_factory = ObjectCreateFabric(
    HiddenItem,
    fields={
        "item": "Введите название товара:",
        "details": "Введите описание:",
        "price": "Введите стоимость:",
        "unit": "Введите, в чем измеряется (шт, гр):",
    },
    command_name="create_item",
    dp=dp,
)


async def main():
    await register_notifiers()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
