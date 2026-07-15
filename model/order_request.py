from pydantic import BaseModel, Field


class OrderRequest(BaseModel):
    item_id: int
    item_quantity: int = Field(gt=0)

