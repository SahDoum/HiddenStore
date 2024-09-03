from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, types
from aiogram.types.callback_query import CallbackQuery
from aiogram.filters.callback_data import CallbackData

from aiogram import Dispatcher

import logging


from init import dp, bot
from data import PageCallback

from data import PageCallback


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ObjectShowView:
    DefaultStartFilter = "show"

    def __init__(self, object_type, prefix: str, dp: Dispatcher):
        self.object_type = object_type
        self.dp = dp

        self.methods: dict[str, str] = {}

        class ActionsCallback(CallbackData, prefix=prefix):
            object_id: str
            action: str

        self.callback = ActionsCallback

    def register(self, name: str, description: str):
        def decorator(func):
            self.methods[name] = description
            dp.callback_query(self.callback.filter(F.action == name))(func)
            return func

        return decorator

    def register_start(self, func):

        @dp.callback_query(self.callback.filter(F.action == self.DefaultStartFilter))
        async def show_func(
            callback_query: types.CallbackQuery, callback_data: self.callback
        ):
            obj = await self.object_type.get(callback_data.object_id)

            if obj is None:
                await callback_query.answer(f"Заказ потерялся. Что-то пошло не так")
                return

            keyboard = self.keyboard(callback_data.object_id)
            msg = await func(obj)

            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=msg,
                reply_markup=keyboard,
            )

        return func

    def keyboard(self, object_id: str):
        builder = InlineKeyboardBuilder()

        for name, description in self.methods.items():
            builder.button(
                text=description,
                callback_data=self.callback(action=name, object_id=object_id),
            )
        # rewrite
        builder.button(text="<< К списку заказов", callback_data=PageCallback(page=0))
        # builder.adjust(-1, 1)

        return builder.as_markup()
