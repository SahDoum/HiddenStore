from libs.models import models
from libs.hidden_redis import HiddenRedis

from config import REDIS_HOST, REDIS_PORT
from api import UserAPI, OrderAPI


redis_client = HiddenRedis(host=REDIS_HOST, port=REDIS_PORT)


async def notify(notify_type: str, user_id=None, order_id=None):
    user = None
    order = None
    if user_id:
        user = await UserAPI.get(user_id)
    if order_id:
        order = await OrderAPI.get(order_id)
    if order is not None and user is None:
        user = models.User()
        user.id = order.user
    await redis_client.publish(notify_type, user, order)
