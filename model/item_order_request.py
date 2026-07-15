from pydantic import BaseModel, Field


class ItemOrderRequest(BaseModel):
    item_id: int
    item_quantity: int = Field(gt=0)
