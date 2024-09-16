import logging
from aiogram import types
from aiogram.fsm.context import FSMContext


from libs.hidden_client import HiddenItem
from libs.models.schemas import OrderItemUpdate

from init import dp
from object_create_view import ObjectCreateView

from object_show_view import ObjectShowView
from paginator_view import Paginator


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


async def description_func(items: list[HiddenItem], first_index: int):
    order_msgs = []
    for hidden_item in items:
        first_index += 1
        order_msgs.append(f"{first_index}. {hidden_item.data.item}")
    msg = "Пункты меню: \n\n" + "\n".join(order_msgs)
    return msg


item_show_view = ObjectShowView(HiddenItem, "item", dp)
items_callback = item_show_view.callback


@item_show_view.register_start
async def order_show_message(hidden_item):
    msg = f"{hidden_item.data}"

    return msg


@item_show_view.register_callback("edit_name", "Изменить название")
async def item_edit_name_button(
    callback_query: types.CallbackQuery,
    callback_data: items_callback,
    state: FSMContext,
    view: ObjectShowView,
):
    await view.set_state(state, "edit_name", callback_data.object_id)
    await callback_query.message.reply("Введите новое название:")


@item_show_view.register_reply("edit_name")
async def item_edit_name(
    message: types.Message,
    state: FSMContext,
    view: ObjectShowView,
):
    state_data = await state.get_data()
    obj_id = state_data["obj_id"]
    hidden_item = await HiddenItem.get(id=obj_id)
    await state.clear()

    if hidden_item is None:
        await message.answer(f"что-то пошло не так")
        return

    res = await hidden_item.update(OrderItemUpdate(item=message.text))

    if not res:
        await message.answer(f"что-то пошло не так")
        return

    await message.answer(f"Обновлено на: {message.text}")


@item_show_view.register_callback("edit_description", "Изменить описание")
async def item_edit_description_button(
    callback_query: types.CallbackQuery,
    callback_data: items_callback,
    state: FSMContext,
    view: ObjectShowView,
):
    await view.set_state(state, "edit_description", callback_data.object_id)
    await callback_query.message.reply("Введите новое описание:")


@item_show_view.register_reply("edit_description")
async def item_edit_description(
    message: types.Message,
    state: FSMContext,
    view: ObjectShowView,
):
    state_data = await state.get_data()
    obj_id = state_data["obj_id"]
    hidden_item = await HiddenItem.get(id=obj_id)
    await state.clear()

    if hidden_item is None:
        await message.answer(f"что-то пошло не так")
        return

    res = await hidden_item.update(OrderItemUpdate(details=message.text))

    if not res:
        await message.answer(f"что-то пошло не так")
        return

    await message.answer(f"Обновлено на: {message.text}")


@item_show_view.register_callback("edit_price", "Изменить цену")
async def item_edit_price_button(
    callback_query: types.CallbackQuery,
    callback_data: items_callback,
    state: FSMContext,
    view: ObjectShowView,
):
    await view.set_state(state, "edit_price", callback_data.object_id)
    await callback_query.message.reply("Введите новую цену:")


@item_show_view.register_reply("edit_price")
async def item_edit_price(
    message: types.Message,
    state: FSMContext,
    view: ObjectShowView,
):
    state_data = await state.get_data()
    obj_id = state_data["obj_id"]
    hidden_item = await HiddenItem.get(id=obj_id)
    await state.clear()

    if hidden_item is None:
        await message.answer(f"что-то пошло не так")
        return

    new_price = 0
    try:
        new_price = int(message.text)
    except:
        await message.answer(f"не число")
        return

    res = await hidden_item.update(OrderItemUpdate(price=new_price))

    if not res:
        await message.answer(f"что-то пошло не так")
        return

    await message.answer(f"Обновлено на: {message.text}")


orders_paginator = Paginator(
    HiddenItem, item_show_view, "item", description_func, "items", dp
)

logger.info("Item View registered")
