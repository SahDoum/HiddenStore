import logging
from aiogram import types
from aiogram.filters import Command

from libs.hidden_client import (
    HiddenUser,
    HiddenOrder,
    HiddenMenu,
    HiddenItem,
    OrderItem,
    HiddenPickupPoint,
)


from utils import get_orders_page, get_order_messages
from keyboards import (
    orders_pagination_keyboard,
    delete_pickup_point_keyboard,
)
from init import dp

from handlers.callbacks import orders_view
from object_create_view import ObjectCreateView


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


pickup_point_factory = ObjectCreateView(
    HiddenPickupPoint,
    fields={
        "address": "Введите адрес пункта самовывоза:",
        "description": "Введите описание пункта самовывоза:",
    },
    command_name="create_pickup_point",
    dp=dp,
)

menu_item_factory = ObjectCreateView(
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


@dp.message(Command("orders"))
async def cmd_orders(message: types.Message):
    orders = await HiddenOrder.list()
    if orders is None:
        await message.reply("Нет заказов")
        return

    orders_page = get_orders_page(orders, 0)
    order_msgs = await get_order_messages(orders_page)

    msg = "Заказы: \n\n" + "\n".join(order_msgs)

    keyboard = orders_pagination_keyboard(orders, 0, orders_view.callback)
    logger.error(msg)

    await message.reply(msg, reply_markup=keyboard)


# /delete_pickup_point command handler
@dp.message(Command("delete_pickup_point"))
async def cmd_delete_pickup_point(message: types.Message):
    # Fetch all pickup points
    pickup_points = await HiddenPickupPoint.get_all()

    if not pickup_points:
        await message.answer("Нет доступных пунктов самовывоза для удаления.")
        return

    # Build the inline keyboard with pickup points
    keyboard = delete_pickup_point_keyboard(pickup_points)

    await message.answer(
        "Выберите пункт самовывоза для удаления:", reply_markup=keyboard
    )


logger.info("Commands registered")
