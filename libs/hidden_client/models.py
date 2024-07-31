from typing import List, Optional
from .client import APIClient

import sys
import os
sys.path.append(os.path.abspath('.'))
from libs.schemas import UserCreate, OrderCreate, OrderUpdate
from libs.models import OrderItem

class HiddenUser:
    def __init__(self, id: str, name: str, telegram_id: str):
        self.id = id
        self.name = name
        self.telegram_id = telegram_id

    @classmethod
    async def get_or_create(cls, id: Optional[str] = None, telegram_id: Optional[str] = None):
        api_client = APIClient()
        user = None
        if id:
            user = await api_client.get_user_by_id(user_id=id)
        elif telegram_id:
            user = await api_client.get_user_by_telegram_id(telegram_id=telegram_id)
        
        if not user and telegram_id:
            user_data = UserCreate(name="Default Name", telegram_id=telegram_id)
            user = await api_client.create_user(user_data=user_data)
        
        await api_client.close()

        if user:
            return cls(id=user["id"], name=user["name"], telegram_id=user["telegram_id"])
        else:
            raise ValueError("User creation failed.")

    async def get_orders(self):
        api_client = APIClient()
        orders = await api_client.get_orders_by_user(user_id=self.id)
        await api_client.close()
        return [HiddenOrder(**order) for order in orders]

class HiddenOrder:
    def __init__(self, id: str, items: List[OrderItem], price: int, status: str, comment: Optional[str], review: Optional[str], is_delivered: bool, is_paid: bool, user: str):
        self.id = id
        self.items = items
        self.price = price
        self.status = status
        self.comment = comment
        self.review = review
        self.is_delivered = is_delivered
        self.is_paid = is_paid
        self.user = user

    @classmethod
    async def create(cls, items: List[OrderItem], price: int, user: str, comment: Optional[str] = None):
        api_client = APIClient()
        order_data = OrderCreate(items=items, price=price, user=user, comment=comment)
        order = await api_client.create_order(order_data=order_data)
        await api_client.close()
        return cls(id=order["id"], items=order["items"], price=order["price"], status=order["status"], comment=order["comment"], review=order["review"], is_delivered=order["is_delivered"], is_paid=order["is_paid"], user=order["user"])

    async def update(self, review: Optional[str] = None, comment: Optional[str] = None, is_delivered: Optional[bool] = None, is_paid: Optional[bool] = None, price: Optional[int] = None, status: Optional[str] = None):
        api_client = APIClient()
        order_update = OrderUpdate(review=review, comment=comment, is_delivered=is_delivered, is_paid=is_paid, price=price, status=status)
        updated_order = await api_client.update_order(order_id=self.id, order_update=order_update)
        await api_client.close()

        self.review = updated_order["review"]
        self.comment = updated_order["comment"]
        self.is_delivered = updated_order["is_delivered"]
        self.is_paid = updated_order["is_paid"]
        self.price = updated_order["price"]
        self.status = updated_order["status"]
        return self

class HiddenMenu:
    def __init__(self, items: List[OrderItem]):
        self.items = items

    @classmethod
    async def get_items(cls):
        api_client = APIClient()
        items = await api_client.get_menu_items()
        await api_client.close()
        return cls(items)

    async def update_items(self):
        api_client = APIClient()
        success = await api_client.update_menu_items(items=self.items)
        await api_client.close()
        return success
