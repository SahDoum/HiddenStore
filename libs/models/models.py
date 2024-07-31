import uuid
from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, Any, List
import datetime
from enum import Enum
from pydantic import BaseModel


import json
from sqlalchemy import TypeDecorator, VARCHAR


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

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"

class OrderItem(BaseObject, table=True):
    __tablename__ = "menu"
    item: str
    amount: Optional[int]
    details: Optional[str] = None
    price: int
    unit: str


# Define a custom type decorator for handling JSON lists of pairs
class JSONListOfPairs(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        # Convert list of pairs to JSON string
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        # Convert JSON string back to list of pairs
        return json.loads(value)

class Order(BaseObject, table=True):
    __tablename__ = "orders"
    items: list[tuple[str, float]] = Field(default=[], sa_column=Column(JSONListOfPairs))  # List of pairs (OrderItem ID, amount)
    price: int
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    comment: Optional[str] = None
    review: Optional[str] = None
    is_delivered: bool = Field(default=False)
    is_paid: bool = Field(default=False)
    user: str = Field(default=None, foreign_key="users.id")
