from typing import Optional
from pydantic import BaseModel


class UserFavoriteItem(BaseModel):
    id: Optional[int] = None
    user_id: int
    item_id: int
