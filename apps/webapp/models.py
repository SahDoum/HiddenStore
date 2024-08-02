from pydantic import BaseModel

class RequestData(BaseModel):
    _auth: str = ""
    user_id: str = ""
    initDataHash: str = ""
    dataCheckString: str = ""

class OrderData(RequestData):
    comment: str = ""
    items: dict[str, float] = {}
    price: int = 0
