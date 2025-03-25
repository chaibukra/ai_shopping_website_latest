from typing import List

from pydantic import BaseModel

from model.item import Item


class OrderResponse(BaseModel):
    items: List[Item]
    shipping_address: str
    order_total_price: float
