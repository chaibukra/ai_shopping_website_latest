from pydantic import BaseModel


class AuthResponse(BaseModel):
    jwt_token: str
    jwt_refresh_token: str = None

