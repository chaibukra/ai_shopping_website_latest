from typing import Optional

from pydantic import BaseModel, Field


class Item(BaseModel):
    item_id: Optional[int] = None
    item_name: str
    price: float
    quantity: int = Field(gt=0)
    image: Optional[str]
