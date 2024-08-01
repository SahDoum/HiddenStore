from aiogram.utils import executor
from init import dp
from handlers.commands import register_handlers
from handlers.callbacks import register_callbacks

if __name__ == '__main__':
    register_handlers()
    register_callbacks()
    executor.start_polling(dp, skip_updates=True)
