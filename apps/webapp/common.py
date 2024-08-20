import hmac
from urllib.parse import unquote
from hashlib import sha256
from fastapi import HTTPException

from models import RequestData
from libs.hidden_client import (
    HiddenUser,
    HiddenOrder,
    HiddenMenu,
    HiddenItem,
    OrderItem,
)

from config import TOKEN


secret_key = hmac.new(b"WebAppData", bytes(TOKEN, encoding="utf-8"), sha256).digest()


def is_valid_data(request: RequestData) -> bool:
    if request.dataCheckString == "" or request.initDataHash == "":
        return False

    data_check_string_unquote = unquote(request.dataCheckString.replace("&", "\n"))
    tg_hash = hmac.new(
        secret_key, bytes(data_check_string_unquote, encoding="utf-8"), sha256
    ).hexdigest()

    if tg_hash == request.initDataHash:
        return True
    else:
        return False


async def make_items(items: dict[str, float]) -> list[tuple[OrderItem, float]]:
    res: list[tuple[OrderItem, float]] = []
    for item_id, count in items.items():
        try:
            hidden_item = await HiddenItem.get(item_id)
            if hidden_item is None or hidden_item.item is None:
                raise HTTPException(status_code=400, detail=f"Item {item_id} not found")
            res.append((hidden_item.item, count))
        except Exception as e:
            raise e
    return res


def get_price(items: dict[str, float]) -> int:
    return 0
