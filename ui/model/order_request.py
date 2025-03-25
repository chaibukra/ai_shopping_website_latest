from pydantic import BaseModel


class OrderRequest(BaseModel):
    item_id: int
    item_quantity: int

