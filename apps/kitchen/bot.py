from aiogram.utils import executor
from init import dp
from apps.kitchen.handlers.notifiers import register_notifiers
import handlers.callbacks
import handlers.commands


if __name__ == "__main__":
    register_notifiers()
    executor.start_polling(dp, skip_updates=True)
