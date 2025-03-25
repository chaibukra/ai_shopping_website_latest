from typing import Optional
from pydantic import BaseModel

from model.role import Role
from model.user_gender import UserGender


class User(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    gender: UserGender
    age: int
    email: str
    phone: str
    address: str
    username: str
    hashed_password: str
    role: Role = Role.USER
