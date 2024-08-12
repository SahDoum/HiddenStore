import asyncio
import json
import logging
import redis.asyncio as redis
import async_timeout
from typing import Union

from libs.models.models import User, Order

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HiddenRedis:
    def __init__(self, host: str, port: int):
        self.redis_client = redis.Redis(host=host, port=port)
        self.channel = "order-update"

    async def publish(
        self, msg_type: str, user: Union[User, None], order: Union[Order, None]
    ):
        # Serialize the message
        message = json.dumps(
            {
                "type": msg_type,
                "user_id": user.id if user else "",
                "order_id": order.id if order else "",
            }
        )
        await self.redis_client.publish(self.channel, message)

    def listen(self, msg_type: str, callback):
        asyncio.create_task(self._handle_notification(msg_type, callback))
        logger.info(f'Listen for type "{msg_type}"')

    async def _handle_notification(self, msg_type: str, callback):
        logger.info(f'Redis handler started for type "{msg_type}"')
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe(self.channel)

        while True:
            try:
                async with async_timeout.timeout(1):
                    message = await pubsub.get_message()
                    if message and message["type"] == "message":
                        try:
                            data = json.loads(message["data"])
                            if data.get("type") == msg_type:
                                await self._process_callback(callback, data)
                        except json.JSONDecodeError as e:
                            logger.error(f"JSON decode error: {e}")
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                logger.error(f"Unexpected error: {e}")

    async def _process_callback(self, callback, data):
        user_id = data.get("user_id")
        order_id = data.get("order_id")
        await callback(user_id, order_id)
