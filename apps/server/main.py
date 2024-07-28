from fastapi import FastAPI, HTTPException
from . import schemas, crud, models

app = FastAPI()

@app.post("/users/", response_model=models.User)
async def create_user(user: schemas.UserCreate):
    existing_user = await crud.get_user_by_telegram_id(telegram_id=user.telegram_id)
    if existing_user:
        raise HTTPException(status_code=400, detail="Telegram ID already registered")
    return await crud.create_user(user=user)

@app.get("/users/", response_model=list[models.User])
async def get_users():
    users = await crud.get_users()
    return users

@app.get("/users/{user_id}", response_model=models.User)
async def get_user_by_id(user_id: str):
    user = await crud.get_user(user_id=user_id,)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/telegram/{telegram_id}", response_model=models.User)
async def get_user_by_telegram_id(telegram_id: str):
    user = await crud.get_user_by_telegram_id(telegram_id=telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=models.User)
async def update_user(user_id: str, user_update: schemas.UserUpdate):
    user = await crud.update_user(user_id=user_id, user_update=user_update)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}", response_model=bool)
async def delete_user(user_id: str):
    success = await crud.delete_user(user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success

@app.post("/orders/", response_model=models.Order)
async def create_order(order: schemas.OrderCreate):
    return await crud.create_order(order=order)

@app.get("/orders/", response_model=list[models.Order])
async def get_orders():
    orders = await crud.get_orders()
    return orders

@app.get("/orders/user/{user_id}", response_model=list[models.Order])
async def get_orders_by_user(user_id: str):
    orders = await crud.get_orders_by_user(user_id=user_id)
    return orders

@app.put("/orders/{order_id}", response_model=models.Order)
async def update_order(order_id: str, order_update: schemas.OrderUpdate):
    order = await crud.update_order(order_id=order_id, order_update=order_update)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.delete("/orders/{order_id}", response_model=bool)
async def delete_order(order_id: str):
    success = await crud.delete_order(order_id=order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return success
