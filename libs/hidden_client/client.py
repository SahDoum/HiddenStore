import httpx
from libs.models.schemas import (
    UserCreate,
    UserUpdate,
    OrderCreate,
    OrderUpdate,
    OrderItemCreate,
    OrderItemUpdate,
    # PaymentUpdate,
    PickupPointCreate,
    PickupPointUpdate,
    PaymentIntentCreate,
    PaymentIntentUpdate,
    DeliveryDetailsCreate,
    DeliveryDetailsUpdate,
)
from .config import APIConfig


class APIClient:
    def __init__(self):
        self.base_url = APIConfig.base_url
        self.api_key = APIConfig.api_key
        self.client = httpx.AsyncClient(base_url=self.base_url)

    def _get_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()

    async def close(self):
        await self.client.aclose()

    # User methods
    async def create_user(self, user_data: UserCreate):
        response = await self.client.post(
            "/users/", json=user_data.dict(), headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    async def get_users(self) -> list[dict]:
        response = await self.client.get("/users/", headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    async def get_user_by_id(self, user_id: str) -> dict:
        response = await self.client.get(
            f"/users/{user_id}", headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    async def get_user_by_telegram_id(self, telegram_id: str) -> dict:
        response = await self.client.get(
            f"/users/telegram/{telegram_id}", headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    async def update_user(self, user_id: str, user_update: UserUpdate):
        response = await self.client.put(
            f"/users/{user_id}",
            json=user_update.dict(exclude_unset=True),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def delete_user(self, user_id: str) -> bool:
        response = await self.client.delete(
            f"/users/{user_id}", headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    # Order methods
    async def create_order(self, order_data: OrderCreate):
        response = await self.client.post(
            "/orders/", json=order_data.dict(), headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    async def get_orders(self) -> list[dict]:
        response = await self.client.get("/orders/", headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    async def get_order_by_id(self, order_id: str) -> dict:
        response = await self.client.get(
            f"/orders/{order_id}", headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    async def get_orders_by_user(self, user_id: str) -> list[dict]:
        response = await self.client.get(
            f"/orders/user/{user_id}", headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    async def update_order(self, order_id: str, order_update: OrderUpdate):
        response = await self.client.put(
            f"/orders/{order_id}",
            json=order_update.dict(exclude_unset=True),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def delete_order(self, order_id: str) -> bool:
        response = await self.client.delete(
            f"/orders/{order_id}", headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    # Menu items methods
    async def get_menu_items(self) -> list[dict]:
        response = await self.client.get("/menu/items", headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    async def create_menu_item(self, item_data: OrderItemCreate) -> dict:
        response = await self.client.post(
            "/menu/items", json=item_data.dict(), headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    async def get_menu_item(self, item_id: str) -> dict:
        response = await self.client.get(
            f"/menu/items/{item_id}", headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    async def update_menu_item(self, item_id: str, item_data: OrderItemUpdate) -> dict:
        response = await self.client.put(
            f"/menu/items/{item_id}",
            json=item_data.dict(exclude_unset=True),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def delete_menu_item(self, item_id: str) -> bool:
        response = await self.client.delete(
            f"/menu/items/{item_id}", headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    # Delivery Details methods
    async def create_delivery_details(
        self, delivery_details_data: DeliveryDetailsCreate
    ) -> dict:
        response = await self.client.post(
            "/orders/delivery_details/",
            json=delivery_details_data.dict(exclude_unset=True),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def get_delivery_details_by_id(self, delivery_details_id: str) -> dict:
        response = await self.client.get(
            f"/orders/delivery_details/{delivery_details_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def update_delivery_details(
        self, delivery_details_id: str, delivery_details_data: DeliveryDetailsUpdate
    ):
        response = await self.client.put(
            f"/orders/delivery_details/{delivery_details_id}",
            json=delivery_details_data.dict(exclude_unset=True),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def delete_delivery_details(self, delivery_details_id: str) -> bool:
        response = await self.client.delete(
            f"/orders/delivery_details/{delivery_details_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    # Payment Intent methods
    async def create_payment_intent(
        self, payment_intent_data: PaymentIntentCreate
    ) -> dict:
        response = await self.client.post(
            "/orders/payment_intent/",
            json=payment_intent_data.dict(exclude_unset=True),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def get_payment_intent_by_id(self, payment_intent_id: str) -> dict:
        response = await self.client.get(
            f"/orders/payment_intent/{payment_intent_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def update_payment_intent(
        self, payment_intent_id: str, payment_intent_data: PaymentIntentUpdate
    ):
        response = await self.client.put(
            f"/orders/payment_intent/{payment_intent_id}",
            json=payment_intent_data.dict(exclude_unset=True),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def delete_payment_intent(self, payment_intent_id: str) -> bool:
        response = await self.client.delete(
            f"/orders/payment_intent/{payment_intent_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    # Pickup Point methods
    async def create_pickup_point(self, pickup_point_data: PickupPointCreate) -> dict:
        response = await self.client.post(
            "/pickuppoints/",
            json=pickup_point_data.dict(exclude_unset=True),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def get_pickup_point_by_id(self, pickup_point_id: str) -> dict:
        response = await self.client.get(
            f"/pickuppoints/{pickup_point_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def get_pickup_points(self) -> list[dict]:
        response = await self.client.get(
            f"/pickuppoints/",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def update_pickup_point(
        self, pickup_point_id: str, pickup_point_data: PickupPointUpdate
    ) -> dict:
        response = await self.client.put(
            f"/pickuppoints/{pickup_point_id}",
            json=pickup_point_data.dict(exclude_unset=True),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    async def delete_pickup_point(self, pickup_point_id: str) -> bool:
        response = await self.client.delete(
            f"/pickuppoints/{pickup_point_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()
