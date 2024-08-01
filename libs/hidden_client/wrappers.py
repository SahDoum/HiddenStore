import logging

from typing import Optional, List
import json

from .client import APIClient
from libs.models.schemas import UserCreate, OrderCreate, OrderUpdate
from libs.models.models import OrderItem, Order, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class HiddenUser:
    def __init__(self, user: User):
        self.user = user

    @classmethod
    async def get_or_create(cls, id: Optional[str] = None, telegram_id: Optional[str] = None):
        async with APIClient() as api_client:
            try:
                user = None
                if id:
                    user = await api_client.get_user_by_id(user_id=id)
                elif telegram_id:
                    user = await api_client.get_user_by_telegram_id(telegram_id=telegram_id)
            except Exception as e:
                if telegram_id:
                    user_data = UserCreate(name="Default Name", telegram_id=telegram_id)
                    user = await api_client.create_user(user_data=user_data)
            finally:
                return cls(User.parse_obj(user))

    async def get_orders(self) -> List[Order]:
        async with APIClient() as api_client:
            try:
                orders = await api_client.get_orders_by_user(user_id=self.user.id)
                return [Order.parse_obj(order) for order in orders]
            except:
                return []

class HiddenOrder:
    def __init__(self, order: Order, user: HiddenUser = None):
        self.order = order
        self.user = user

    @classmethod
    async def create(cls, items: list[tuple[OrderItem, float]], price: int, user: HiddenUser, comment: Optional[str] = None):
        async with APIClient() as api_client:
            order_data = OrderCreate(
                items=[(cls.item_to_str(item[0]), item[1]) for item in items],  # Convert OrderItem to dict and keep count
                price=price,
                user=user.user.id,  # Use the user ID from HiddenUser
                comment=comment
            )
            order = await api_client.create_order(order_data=order_data)
        return cls(Order.parse_obj(order))

    async def update(self, review: Optional[str] = None, comment: Optional[str] = None, is_delivered: Optional[bool] = None, is_paid: Optional[bool] = None, price: Optional[int] = None, status: Optional[str] = None):
        async with APIClient() as api_client:
            order_update = OrderUpdate(review=review, comment=comment, is_delivered=is_delivered, is_paid=is_paid, price=price, status=status)
            updated_order = await api_client.update_order(order_id=self.order.id, order_update=order_update)
        self.order = Order.parse_obj(updated_order)
        return self.order
    
    @staticmethod
    def item_to_str(item: OrderItem) -> str:
        return json.dumps(item.model_dump(mode='json'))
    
    @staticmethod
    def str_to_item(item_str: str) -> OrderItem:
        logger.error(json.loads(item_str))
        return OrderItem.parse_obj(json.loads(item_str))
    
    def items(self) -> list[tuple[OrderItem, float]]:
        return [(self.str_to_item(item), count) for item, count in self.order.items]

class HiddenMenu:
    def __init__(self, items: List[OrderItem]):
        self.items = items

    @classmethod
    async def get_items(cls):
        async with APIClient() as api_client:
            items = await api_client.get_menu_items()
        return cls([OrderItem.parse_obj(item) for item in items])

    async def update_items(self):
        async with APIClient() as api_client:
            success = await api_client.update_menu_items(items=[item.dict() for item in self.items])
        return success
