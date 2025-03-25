from pydantic import BaseModel


class ItemOrderRequest(BaseModel):
    item_id: int
    item_quantity: int
