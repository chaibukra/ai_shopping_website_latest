from pydantic import BaseModel

from config.config import Config

config = Config()


class AuthResponse(BaseModel):
    jwt_token: str
    jwt_refresh_token: str = None
    expires_in: float = config.TOKEN_EXPIRY_TIME * 60
    refresh_expires_in: int = 1 * 24 * 60 * 60
