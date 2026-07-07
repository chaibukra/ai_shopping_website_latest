import datetime
import uuid
from typing import Optional

from fastapi import HTTPException
from jose import jwt, JWTError
from starlette import status

from config.config import Config
from exceptions.security_exceptions import token_exception
from model.auth_response import AuthResponse
from model.user import User
from redisClient.redis_client import redis_client
from service import user_service

config = Config()


async def authenticate_user(username: str, password: str):
    user = await user_service.get_by_username(username)
    if user and user_service.verify_password(password, user.hashed_password):
        return user
    else:
        return False


async def create_access_token(user: User) -> str:
    token_expire_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=config.TOKEN_EXPIRY_TIME)
    user_data = {"subject": user.username, "id": user.id, "role": user.role.value, "exp": token_expire_time}
    token = jwt.encode(user_data, config.SECRET_KEY, config.ALGORITHM)
    return token


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


async def create_refresh_token(user: User) -> str:
    token_expire_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
    jti = str(uuid.uuid4())
    user_data = {"subject": user.username, "id": user.id, "jti": jti, "type": "refresh", "exp": token_expire_time}
    token = jwt.encode(user_data, config.SECRET_KEY, config.ALGORITHM)

    await redis_client.set(f"refresh:{jti}", str(user.id), ex=60 * 60 * 24 * 1)

    return token


async def create_access_and_refresh_token(user: User) -> AuthResponse:
    access_token = await create_access_token(user)
    refresh_token = await create_refresh_token(user)
    return AuthResponse(jwt_token=access_token, jwt_refresh_token=refresh_token)


async def validate_and_revoke_refresh_token(token: str) -> Optional[User]:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, config.ALGORITHM)
        if payload["type"] != "refresh":
            raise token_exception()

        jti = payload.get("jti")
        key = f"refresh:{jti}"

        exists = await redis_client.exists(key)

        if not exists:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")

        await redis_client.delete(key)

        username = payload.get("subject")
        user = await user_service.get_by_username(username)

        return user

    except JWTError:
        token_exception()
