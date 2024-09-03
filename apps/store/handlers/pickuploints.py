import logging
from aiogram.filters import Command
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


from libs.hidden_client import HiddenPickupPoint

from init import dp, bot
from object_create_view import ObjectCreateView


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Callback data for pickup point deletion
class PickupPointDeleteCallback(CallbackData, prefix="delete_pickup_point"):
    pickup_point_id: str


def delete_pickup_point_keyboard(pickup_points: list):
    builder = InlineKeyboardBuilder()

    for pickup_point in pickup_points:
        builder.button(
            text=pickup_point.pickup_point.address,
            callback_data=PickupPointDeleteCallback(
                pickup_point_id=pickup_point.pickup_point.id
            ),
        )

    return builder.as_markup()


pickup_point_factory = ObjectCreateView(
    HiddenPickupPoint,
    fields={
        "address": "Введите адрес пункта самовывоза:",
        "description": "Введите описание пункта самовывоза:",
    },
    command_name="create_pickup_point",
    dp=dp,
)


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


# Callback handler for pickup point deletion
@dp.callback_query(PickupPointDeleteCallback.filter())
async def process_delete_pickup_point(
    callback_query: types.CallbackQuery, callback_data: PickupPointDeleteCallback
):
    # Retrieve the pickup point ID
    pickup_point_id = callback_data.pickup_point_id

    # Placeholder: Call the delete method for the selected pickup point
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


logger.info("Pickup Point View registered")
