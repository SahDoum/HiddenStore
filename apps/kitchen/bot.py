from aiogram.utils import executor
from init import dp
from handlers.commands import register_handlers
from apps.kitchen.handlers.notifiers import register_notifiers
import handlers.callbacks


if __name__ == '__main__':
    register_handlers()
    register_notifiers()
    executor.start_polling(dp, skip_updates=True)
