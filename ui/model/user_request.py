from pydantic import BaseModel

from model.user_gender import UserGender


class UserRequest(BaseModel):
    first_name: str
    last_name: str
    gender: UserGender
    age: int
    email: str
    phone: str
    country: str
    city: str
    username: str
    password: str
