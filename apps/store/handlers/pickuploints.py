import logging
from typing import Optional
from aiogram import types
from aiogram.fsm.context import FSMContext


from libs.hidden_client import HiddenPickupPoint

from paginator_view import Paginator
from object_show_view import ObjectShowView
from init import dp, bot, render_template
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


pickuppoint_view = ObjectShowView(HiddenPickupPoint, "pickuppoint", dp)
pickuppoint_callback = pickuppoint_view.callback


@pickuppoint_view.register_start
async def order_show_message(hidden_pickuppoint: Optional[HiddenPickupPoint]):
    if hidden_pickuppoint is None:
        return f"Заказ потерялся. Что-то пошло не так"

    msg = hidden_pickuppoint.data.description

    return msg


@pickuppoint_view.register_callback("delete", "Удалить")
async def order_delete_message(
    callback_query: types.CallbackQuery,
    callback_data: pickuppoint_callback,
    state: FSMContext,
    view: ObjectShowView,
):
    pickup_point_id = callback_data.object_id
    point = await HiddenPickupPoint.get(pickup_point_id)

    success = False
    if point:
        success = await point.delete()

    if success:
        await callback_query.answer(f"Пункт самовывоза удален.")
        await bot.edit_message_text(
            text=f"Пункт самовывоза удален.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
        )
    else:
        await callback_query.answer("Ошибка при удалении пункта самовывоза.")


async def description_func(pickuppoints, first_index):
    msgs = []
    for hidden_pickuppoint in pickuppoints:
        first_index += 1
        msgs.append(
            f"{first_index}."
            + render_template(
                "pickuppont_info_short.txt",
                pickuppoint=hidden_pickuppoint.data,
            )
        )
    msg = "Точки самовывоза: \n\n" + "\n".join(msgs)

    return msg


pickuppoint_paginator = Paginator(
    HiddenPickupPoint,
    pickuppoint_view,
    "pickuppoint",
    description_func,
    "pickuppoint",
    dp,
)

logger.info("Pickup Point View registered")
