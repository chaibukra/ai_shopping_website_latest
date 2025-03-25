import datetime
from typing import Optional
from jose import jwt, JWTError
from config.config import Config
from exceptions.security_exceptions import token_exception
from model.auth_response import AuthResponse
from model.user import User
from service import user_service

config = Config()


async def authenticate_user(username: str, password: str):
    user = await user_service.get_by_username(username)
    if user and user_service.verify_password(password, user.hashed_password):
        return user
    else:
        return False


async def create_access_token(user: User) -> AuthResponse:
    token_expire_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=config.TOKEN_EXPIRY_TIME)
    user_data = {"subject": user.username, "id": user.id, "role": user.role.value, "exp": token_expire_time}
    token = jwt.encode(user_data, config.SECRET_KEY, config.ALGORITHM)
    return AuthResponse(jwt_token=token)


async def validate_token(token: str) -> Optional[User]:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, config.ALGORITHM)
        username = payload.get("subject")
        if username:
            return await user_service.get_by_username(username)
        else:
            return None
    except JWTError:
        token_exception()


async def token_get_user_role(token: str) -> Optional[User]:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, config.ALGORITHM)
        username = payload.get("subject")
        if username:
            return payload.get("role")
        else:
            return None
    except JWTError:
        token_exception()
