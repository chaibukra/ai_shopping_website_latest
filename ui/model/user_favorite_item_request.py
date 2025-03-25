from pydantic import BaseModel


class UserFavoriteItemRequest(BaseModel):
    item_name: str
