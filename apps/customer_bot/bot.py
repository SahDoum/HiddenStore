from aiogram.utils import executor
from init import dp
from handlers.commands import register_handlers

if __name__ == '__main__':
    register_handlers()
    executor.start_polling(dp, skip_updates=True)
