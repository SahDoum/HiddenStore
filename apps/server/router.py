from typing import Any

from fastapi import FastAPI, HTTPException
from libs.models import models
from libs.models import schemas
from api import UserAPI, OrderAPI, ItemsAPI

app = FastAPI()

@app.post("/users/", response_model=models.User)
async def create_user(user: schemas.UserCreate):
    existing_user = await UserAPI.get_by_telegram_id(telegram_id=user.telegram_id)
    if existing_user:
        raise HTTPException(status_code=400, detail="Telegram ID already registered")
    return await UserAPI.create(data=user)

@app.get("/users/", response_model=list[models.User])
async def get_users():
    users = await UserAPI.get_all()
    return users

@app.get("/users/{user_id}", response_model=models.User)
async def get_user_by_id(user_id: str):
    user = await UserAPI.get(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/telegram/{telegram_id}", response_model=models.User)
async def get_user_by_telegram_id(telegram_id: str):
    user = await UserAPI.get_by_telegram_id(telegram_id=telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=models.User)
async def update_user(user_id: str, user_update: schemas.UserUpdate):
    user = await UserAPI.update(user_id=user_id, data=user_update)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}", response_model=bool)
async def delete_user(user_id: str):
    success = await UserAPI.delete(user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success

@app.post("/orders/", response_model=models.Order)
async def create_order(order: schemas.OrderCreate):
    return await OrderAPI.create(data=order)

@app.get("/orders/", response_model=list[models.Order])
async def get_orders():
    orders = await OrderAPI.get_all()
    return orders

@app.get("/orders/user/{user_id}", response_model=list[models.Order])
async def get_orders_by_user(user_id: str):
    orders = await OrderAPI.get_by_user(user_id=user_id)
    return orders

@app.put("/orders/{order_id}", response_model=models.Order)
async def update_order(order_id: str, order_update: schemas.OrderUpdate):
    order = await OrderAPI.update(order_id=order_id, data=order_update)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.delete("/orders/{order_id}", response_model=bool)
async def delete_order(order_id: str):
    success = await OrderAPI.delete(order_id=order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return success

@app.get("/menu/items", response_model=list[models.OrderItem])
async def get_menu_items():
    items = await ItemsAPI.get_all()
    return items

@app.post("/menu/items", response_model=models.OrderItem)
async def create_menu_item(item: schemas.OrderItemCreate):
    return await ItemsAPI.create(data=item)

@app.get("/menu/items/{item_id}", response_model=models.OrderItem)
async def get_menu_item(item_id: str):
    item = await ItemsAPI.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/menu/items/{item_id}", response_model=models.OrderItem)
async def update_menu_item(item_id: str, item: schemas.OrderItemUpdate):
    updated_item = await ItemsAPI.update(item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found or update failed")
    return updated_item

@app.delete("/menu/items/{item_id}", response_model=bool)
async def delete_menu_item(item_id: str):
    success = await ItemsAPI.delete(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found or delete failed")
    return success
