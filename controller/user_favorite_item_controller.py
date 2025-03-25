from typing import Optional, List
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from exceptions.security_exceptions import user_unauthorized_exception
from model.user_favorite_item_request import UserFavoriteItemRequest
from model.user_favorite_item_response import UserFavoriteItemResponse
from service import user_favorite_item_service, auth_service

router = APIRouter(
    prefix="/user_favorite_item",
    tags=["user_favorite_item"],
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_favorite_items_list(token: str = Depends(oauth2_bearer)) -> Optional[List[UserFavoriteItemResponse]]:
    user = await auth_service.validate_token(token)
    if user is None:
        raise user_unauthorized_exception()
    return await user_favorite_item_service.get_favorite_items_list(user)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_favorite_item(user_favorite_item_request: UserFavoriteItemRequest,
                                    token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_token(token)
    if user is None:
        raise user_unauthorized_exception()
    await user_favorite_item_service.create_user_favorite_item(user_favorite_item_request, user)


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_user_favorite_item(user_favorite_item_request: UserFavoriteItemRequest, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_token(token)
    if user is None:
        raise user_unauthorized_exception()
    await user_favorite_item_service.delete_user_favorite_item(user_favorite_item_request, user)

