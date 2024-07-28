import uuid
from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional
import datetime
from enum import Enum

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

class Order(BaseObject, table=True):
    __tablename__ = "orders"
    items: list[dict[str, str]] = Field(sa_column=Column(JSON))
    price: int
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    comment: Optional[str] = None
    review: Optional[str] = None
    is_delivered: bool = Field(default=False)
    is_paid: bool = Field(default=False)
    user: str = Field(default=None, foreign_key="users.id")

# Example structure for the items field
# items = [
#     {"item": "item1", "count": 1, "details": "details1", "price": 100},
#     {"item": "item2", "count": 2, "details": "details2", "price": 200},
#     ...
# ]
