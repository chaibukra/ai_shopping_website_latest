import json
from typing import Optional, List
from fastapi import HTTPException
from passlib.context import CryptContext
from starlette import status
from exceptions.security_exceptions import username_taken_exception
from model.role import Role
from model.user import User
from model.user_request import UserRequest
from repository import user_repository
from service import user_favorite_item_service, order_service

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


async def get_by_user_id(user_id: int) -> Optional[User]:
    user = await user_repository.get_by_user_id(user_id)
    if user is not None:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id : {user_id} Not Found"
        )


async def get_by_username(username: str) -> Optional[User]:
    return await user_repository.get_by_username(username)


async def create_user(user_request: UserRequest):
    if await validate_unique_username(user_request.username):
        hashed_password = get_password_hash(user_request.password)
        user_address = {"country": user_request.country, "city": user_request.city}
        user_address_json_string = json.dumps(user_address)
        user = User(
            id=None,
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            gender=user_request.gender,
            age=user_request.age,
            email=user_request.email,
            phone=user_request.phone,
            address=user_address_json_string,
            username=user_request.username,
            hashed_password=hashed_password
        )
        await user_repository.create_user(user)
    else:
        raise username_taken_exception()


async def validate_unique_username(username: str) -> bool:
    existing_user = await user_repository.get_by_username(username)
    return existing_user is None


async def delete_user(user):
    await user_favorite_item_service.delete_all_user_favorite_items(user)
    await order_service.delete_all_user_orders(user)
    await user_repository.delete_user(user)


async def get_all_users() -> Optional[List[User]]:
    return await user_repository.get_all_users()
