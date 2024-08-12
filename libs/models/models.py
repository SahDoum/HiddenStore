from typing import Optional
import uuid
import json
import datetime

from sqlmodel import SQLModel, Field, Column, JSON
from sqlalchemy import TypeDecorator, VARCHAR

from .statuses import OrderStatus, PaymentStatus


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


class PickupPoint(BaseObject, table=True):
    adress: Optional[str] = None
    description: Optional[str] = None


class Order(BaseObject, table=True):
    __tablename__ = "orders"

    # Common
    status: OrderStatus = Field(default=OrderStatus.CREATED)
    user: str = Field(default=None, foreign_key="users.id")

    # On create
    items: list[tuple[str, float]] = Field(
        default=[], sa_column=Column(JSONListOfPairs)
    )
    price: int
    comment: Optional[str] = None
    is_paid: bool = Field(default=False)
    payment: PaymentStatus = Field(default=PaymentStatus.NONE)

    # On delivery
    details: Optional[str] = None

    # On finish
    review: Optional[str] = None
    is_delivered: bool = Field(default=False)
