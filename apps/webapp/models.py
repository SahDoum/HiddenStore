from pydantic import BaseModel
from libs.hidden_client import PaymentMethod


class RequestData(BaseModel):
    _auth: str = ""
    user_id: str = ""
    initDataHash: str = ""
    dataCheckString: str = ""


class OrderData(RequestData):
    comment: str = ""
    items: dict[str, float] = {}
    price: int = 0
    pickup_point_id: str
    payment_method: str
