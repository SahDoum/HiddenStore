from typing import Optional

class APIConfig:
    base_url: str
    api_key: Optional[str] = None

    @classmethod
    def setup(cls, base_url: str, api_key: Optional[str] = None):
        cls.base_url = base_url
        cls.api_key = api_key
