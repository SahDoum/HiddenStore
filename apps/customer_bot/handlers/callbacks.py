import logging

from libs.hidden_client import HiddenUser
from init import bot, redis_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_create(user_id):
    user = await HiddenUser.get_or_create(id=user_id)
    await bot.send_message(user.user.telegram_id, "Order created") 


def register_callbacks():
    redis_client.listen(msg_type="create", callback=on_create)
