from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    item_id: Optional[int] = None
    item_name: str
    price: float
    quantity: int
    image: str
