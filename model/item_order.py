from typing import Optional
from pydantic import BaseModel, Field


class ItemOrder(BaseModel):
    id: Optional[int] = None
    order_id: int
    item_id: int
    item_quantity: int = Field(gt=0)
