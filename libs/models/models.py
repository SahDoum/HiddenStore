from typing import Optional
import uuid
import json
import datetime

from sqlmodel import SQLModel, Field, Column, JSON
from sqlalchemy import TypeDecorator, VARCHAR

from .statuses import (
    OrderStatus,
    PaymentStatus,
    PaymentMethod,
    DeliveryMethod,
    DeliveryStatus,
)


# Ccustom type decorator for handling JSON lists of pairs
class JSONListOfPairs(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)


# rewrite in pydantic
# without sqlmodel
class BaseObject(SQLModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp_created: datetime.datetime = Field(default_factory=datetime.datetime.now)
    timestamp_updated: datetime.datetime = Field(default_factory=datetime.datetime.now)


class PickupPoint(BaseObject, table=True):
    __tablename__ = "pickuppoints"
    address: Optional[str] = None
    description: Optional[str] = None


class PaymentIntent(BaseObject, table=True):
    __tablename__ = "paymentintents"
    amount: int
    method: PaymentMethod
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    payment_details: Optional[dict] = Field(sa_column=Column(JSON))


class DeliveryDetails(BaseObject, table=True):
    __tablename__ = "deliverydetails"
    method: DeliveryMethod
    status: DeliveryStatus = Field(default=DeliveryStatus.PENDING)
    address: Optional[str] = None  # Для доставки курьером или из точки доставки
    pickup_point_id: Optional[str] = Field(default=None, foreign_key="pickuppoints.id")
    delivery_time: Optional[datetime.datetime] = None
    courier_id: Optional[str] = None  # Если доставка курьером
    additional_info: Optional[str] = None  # Любая дополнительная информация


class User(BaseObject, table=True):
    __tablename__ = "users"
    name: str
    telegram_id: str = Field(unique=True, index=True)


class OrderItem(BaseObject, table=True):
    __tablename__ = "menu"
    item: str
    amount: Optional[int] = None
    details: Optional[str] = None
    price: int
    unit: str
    image: str = "default.png"


class Order(BaseObject, table=True):
    __tablename__ = "orders"

    status: OrderStatus = Field(default=OrderStatus.CREATED)  # Deprecated
    user: str = Field(default=None, foreign_key="users.id")
    items: list[tuple[str, float]] = Field(
        default=[], sa_column=Column(JSONListOfPairs)
    )
    price: int
    comment: Optional[str] = None

    payment_id: Optional[str] = Field(default=None, foreign_key="paymentintents.id")
    delivery_id: Optional[str] = Field(default=None, foreign_key="deliverydetails.id")

    review: Optional[str] = None
    is_delivered: bool = Field(default=False)
