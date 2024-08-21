import logging
from aiogram import types
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext

from libs.hidden_client import (
    HiddenUser,
    HiddenOrder,
    HiddenMenu,
    HiddenItem,
    OrderItem,
    HiddenPickupPoint,
)


from data import PickupPointState
from utils import get_orders_page, get_order_messages
from keyboards import (
    order_keyboard,
    orders_pagination_keyboard,
    delete_pickup_point_keyboard,
)
from init import dp


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message(Command("orders"))
async def cmd_orders(message: types.Message):
    orders = await HiddenOrder.list()
    if orders is None:
        await message.reply("Нет заказов")
        return

    orders_page = get_orders_page(orders, 0)
    order_msgs = await get_order_messages(orders_page)

    msg = "Заказы: \n\n" + "\n".join(order_msgs)

    keyboard = orders_pagination_keyboard(orders, 0)
    logger.error(msg)

    await message.reply(msg, reply_markup=keyboard)


# /create_pickup_point command handler
@dp.message(Command("create_pickup_point"))
async def cmd_create_pickup_point(message: types.Message, state: FSMContext):
    await message.answer("Введите адрес пункта самовывоза:")
    await state.set_state(PickupPointState.address)


# Handler to capture the address input
@dp.message(PickupPointState.address)
async def process_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Введите описание пункта самовывоза:")
    await state.set_state(PickupPointState.description)


# Handler to capture the description input
@dp.message(PickupPointState.description)
async def process_description(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    address = user_data.get("address")
    await state.clear()
    description = message.text

    point = await HiddenPickupPoint.create(address=address, description=description)

    await message.answer(
        f"Пункт самовывоза создан:\n\nАдрес: {point.pickup_point.address}\nОписание: {point.pickup_point.description}"
    )

    # Finish the state


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
