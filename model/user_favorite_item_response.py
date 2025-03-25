from pydantic import BaseModel


class UserFavoriteItemResponse(BaseModel):
    item_name: str
    price: float
    quantity: int
