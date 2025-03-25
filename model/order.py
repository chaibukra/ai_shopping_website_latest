from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from model.order_status import OrderStatus


class Order(BaseModel):
    order_id: Optional[int] = None
    user_id: int
    order_date: datetime
    shipping_address: str
    order_status: OrderStatus
