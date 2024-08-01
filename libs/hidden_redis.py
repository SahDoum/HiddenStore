import asyncio
import json
import logging
import redis.asyncio as redis
import async_timeout

from libs.models.models import User, Order
from libs.hidden_client import HiddenUser, HiddenOrder


# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class HiddenRedis:
    def __init__(self, host: str, port: int):
        self.redis_client = redis.Redis(host=host, port=port)
        self.channel = "order-update"
        self.event_loop = asyncio.get_event_loop()

    async def publish(self, msg_type: str, user: User, order: Order): #, order: HiddenOrder):
        # Serialize the message
        message = json.dumps({
            'type': msg_type,
            'user_id': user.id,
            'order_id': order.id,
            # 'order': order.order.to_dict()  # assuming HiddenOrder has a to_dict method
        })
        await self.redis_client.publish(self.channel, message)

    def listen(self, msg_type: str, callback):
        coro = self._handle_notification(msg_type, callback)
        self.event_loop.create_task(coro())

    def _handle_notification(self, msg_type: str, callback):
        async def notification_handler():
            logger.info(f"Redis handler started for type \"{msg_type}\"")
            pubsub = self.redis_client.pubsub()
            await pubsub.subscribe(self.channel)

            while True:
                try:
                    async with async_timeout.timeout(1):
                        message = await pubsub.get_message()
                        if message and  message["type"] == 'message':
                            try:
                                data = json.loads(message["data"])
                                if data.get('type') == msg_type:
                                    await self._process_callback(callback, data)
                            except json.JSONDecodeError as e:
                                logger.error(f"JSON decode error: {e}")
                except asyncio.TimeoutError:
                    pass
                except Exception as e:
                    logger.error(f"Unexpected error: {e}")

        return notification_handler

    async def _process_callback(self, callback, data):
        user_id = data.get('user_id')
        order_id = data.get('order_id')
        await callback(user_id, order_id)
