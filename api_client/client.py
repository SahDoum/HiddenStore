import httpx
from typing import List, Optional

class APIClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self.client = httpx.Client(base_url=self.base_url)
        
    def _get_headers(self):
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    # User methods
    def create_user(self, name: str, telegram_id: str):
        payload = {"name": name, "telegram_id": telegram_id}
        response = self.client.post("/users/", json=payload, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def get_users(self) -> List[dict]:
        response = self.client.get("/users/", headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def get_user_by_id(self, user_id: str) -> dict:
        response = self.client.get(f"/users/{user_id}", headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_user_by_telegram_id(self, telegram_id: str) -> dict:
        print("send response")
        response = self.client.get(f"/users/telegram/{telegram_id}", headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def update_user(self, user_id: str, name: Optional[str] = None, telegram_id: Optional[str] = None):
        payload = {}
        if name:
            payload["name"] = name
        if telegram_id:
            payload["telegram_id"] = telegram_id
        response = self.client.put(f"/users/{user_id}", json=payload, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def delete_user(self, user_id: str) -> bool:
        response = self.client.delete(f"/users/{user_id}", headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    # Order methods
    def create_order(self, items: List[dict], price: int, user: str, comment: Optional[str] = None):
        payload = {"items": items, "price": price, "user": user, "comment": comment}
        response = self.client.post("/orders/", json=payload, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_orders(self) -> List[dict]:
        response = self.client.get("/orders/", headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def get_order_by_id(self, order_id: str) -> dict:
        response = self.client.get(f"/orders/{order_id}", headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def get_orders_by_user(self, user_id: str) -> List[dict]:
        response = self.client.get(f"/orders/user/{user_id}", headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def update_order(self, order_id: str, review: Optional[str] = None, comment: Optional[str] = None,
                          is_delivered: Optional[bool] = None, is_paid: Optional[bool] = None,
                          price: Optional[int] = None, status: Optional[str] = None):
        payload = {}
        if review:
            payload["review"] = review
        if comment:
            payload["comment"] = comment
        if is_delivered is not None:
            payload["is_delivered"] = is_delivered
        if is_paid is not None:
            payload["is_paid"] = is_paid
        if price:
            payload["price"] = price
        if status:
            payload["status"] = status
        response = self.client.put(f"/orders/{order_id}", json=payload, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def delete_order(self, order_id: str) -> bool:
        response = self.client.delete(f"/orders/{order_id}", headers=self._get_headers())
        response.raise_for_status()
        return response.json()

# # Пример использования
# if __name__ == "__main__":
#     import asyncio

#     def main():
#         client = MyAPIClient(base_url="http://127.0.0.1:8000")
#         users = await client.get_users()
#         print(users)

#     asyncio.run(main())
