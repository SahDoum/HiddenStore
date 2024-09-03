import logging

from fastapi import FastAPI, HTTPException

from libs.models import models
from libs.models import schemas

from api import (
    UserAPI,
    OrderAPI,
    ItemsAPI,
    PickupPointAPI,
    DeliveryDetailsAPI,
    PaymentIntentAPI,
)
from notifier import notify


app = FastAPI()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    res_order = await OrderAPI.create(data=order)
    await notify("create", order_id=res_order.id)
    return order


@app.get("/orders/", response_model=list[models.Order])
async def get_orders():
    orders = await OrderAPI.get_all()
    return orders


@app.get("/orders/user/{user_id}", response_model=list[models.Order])
async def get_orders_by_user(user_id: str):
    orders = await OrderAPI.get_by_user(user_id=user_id)
    return orders


@app.get("/orders/{order_id}", response_model=models.Order)
async def get_order_by_id(order_id: str):
    order = await OrderAPI.get(order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.put("/orders/{order_id}", response_model=models.Order)
async def update_order(order_id: str, order_update: schemas.OrderUpdate):
    order = await OrderAPI.update(order_id=order_id, data=order_update)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    await notify("update", order_id=order.id)
    return order


@app.delete("/orders/{order_id}", response_model=bool)
async def delete_order(order_id: str):
    success = await OrderAPI.delete(order_id=order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")

    await notify("deleted", order_id=order_id)
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


# Pickup Point Endpoints


@app.post("/pickuppoints/", response_model=models.PickupPoint)
async def create_pickup_point(pickup_point: schemas.PickupPointCreate):
    return await PickupPointAPI.create(data=pickup_point)


@app.get("/pickuppoints/", response_model=list[models.PickupPoint])
async def get_pickup_points():
    return await PickupPointAPI.get_all()


@app.get("/pickuppoints/{pickuppoint_id}", response_model=models.PickupPoint)
async def get_pickup_point_by_id(pickuppoint_id: str):
    pickup_point = await PickupPointAPI.get(pickuppoint_id=pickuppoint_id)
    if not pickup_point:
        raise HTTPException(status_code=404, detail="Pickup point not found")
    return pickup_point


@app.put("/pickuppoints/{pickuppoint_id}", response_model=models.PickupPoint)
async def update_pickup_point(
    pickuppoint_id: str, pickup_point_update: schemas.PickupPointUpdate
):
    pickup_point = await PickupPointAPI.update(
        pickuppoint_id=pickuppoint_id, data=pickup_point_update
    )
    if not pickup_point:
        raise HTTPException(
            status_code=404, detail="Pickup point not found or update failed"
        )
    return pickup_point


@app.delete("/pickuppoints/{pickuppoint_id}", response_model=bool)
async def delete_pickup_point(pickuppoint_id: str):
    success = await PickupPointAPI.delete(pickuppoint_id=pickuppoint_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="Pickup point not found or delete failed"
        )
    return success


# Payment Intent Endpoints


@app.post("/paymentintents/", response_model=models.PaymentIntent)
async def create_payment_intent(payment_intent: schemas.PaymentIntentCreate):
    return await PaymentIntentAPI.create(data=payment_intent)


@app.get("/paymentintents/", response_model=list[models.PaymentIntent])
async def get_payment_intents():
    return await PaymentIntentAPI.get_all()


@app.get("/paymentintents/{payment_intent_id}", response_model=models.PaymentIntent)
async def get_payment_intent_by_id(payment_intent_id: str):
    payment_intent = await PaymentIntentAPI.get(payment_intent_id=payment_intent_id)
    if not payment_intent:
        raise HTTPException(status_code=404, detail="Payment intent not found")
    return payment_intent


@app.put("/paymentintents/{payment_intent_id}", response_model=models.PaymentIntent)
async def update_payment_intent(
    payment_intent_id: str, payment_intent_update: schemas.PaymentIntentUpdate
):
    payment_intent = await PaymentIntentAPI.update(
        payment_intent_id=payment_intent_id, data=payment_intent_update
    )
    if not payment_intent:
        raise HTTPException(
            status_code=404, detail="Payment intent not found or update failed"
        )
    return payment_intent


@app.delete("/paymentintents/{payment_intent_id}", response_model=bool)
async def delete_payment_intent(payment_intent_id: str):
    success = await PaymentIntentAPI.delete(payment_intent_id=payment_intent_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="Payment intent not found or delete failed"
        )
    return success


# Delivery Details Endpoints


@app.post("/deliverydetails/", response_model=models.DeliveryDetails)
async def create_delivery_details(delivery_details: schemas.DeliveryDetailsCreate):
    return await DeliveryDetailsAPI.create(data=delivery_details)


@app.get("/deliverydetails/", response_model=list[models.DeliveryDetails])
async def get_delivery_details():
    return await DeliveryDetailsAPI.get_all()


@app.get(
    "/deliverydetails/{delivery_details_id}", response_model=models.DeliveryDetails
)
async def get_delivery_details_by_id(delivery_details_id: str):
    delivery_details = await DeliveryDetailsAPI.get(
        delivery_details_id=delivery_details_id
    )
    if not delivery_details:
        raise HTTPException(status_code=404, detail="Delivery details not found")
    return delivery_details


@app.put(
    "/deliverydetails/{delivery_details_id}", response_model=models.DeliveryDetails
)
async def update_delivery_details(
    delivery_details_id: str, delivery_details_update: schemas.DeliveryDetailsUpdate
):
    delivery_details = await DeliveryDetailsAPI.update(
        delivery_details_id=delivery_details_id, data=delivery_details_update
    )
    if not delivery_details:
        raise HTTPException(
            status_code=404, detail="Delivery details not found or update failed"
        )
    return delivery_details


@app.delete("/deliverydetails/{delivery_details_id}", response_model=bool)
async def delete_delivery_details(delivery_details_id: str):
    success = await DeliveryDetailsAPI.delete(delivery_details_id=delivery_details_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="Delivery details not found or delete failed"
        )
    return success
