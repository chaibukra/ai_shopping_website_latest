from typing import List, Optional
from fastapi import HTTPException
from starlette import status
from model.user import User
from model.user_favorite_item import UserFavoriteItem
from model.user_favorite_item_request import UserFavoriteItemRequest
from model.user_favorite_item_response import UserFavoriteItemResponse
from repository import user_favorite_item_repository
from service import item_service


async def check_if_user_favorite_item_exist(user_favorite_item: UserFavoriteItem) -> bool:
    exist_user_favorite_item = await user_favorite_item_repository.check_if_user_favorite_item_exist(user_favorite_item)
    return exist_user_favorite_item


async def create_user_favorite_item(user_favorite_item_request: UserFavoriteItemRequest, user: User):
    item_id = await item_service.get_item_id_by_item_name(user_favorite_item_request.item_name)
    user_favorite_item = UserFavoriteItem(user_id=user.id,
                                          item_id=item_id)
    exist_user_favorite_item = await check_if_user_favorite_item_exist(user_favorite_item)
    if exist_user_favorite_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provided item has already been added to the user favorite items list"
        )
    else:
        await user_favorite_item_repository.create_user_favorite_item(user_favorite_item)


async def get_favorite_items_list(user) -> Optional[List[UserFavoriteItemResponse]]:
    favorite_items = await user_favorite_item_repository.get_favorite_items_list(user.id)
    if favorite_items is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has not have items in his favorite items list"
        )
    return favorite_items


async def delete_user_favorite_item(user_favorite_item_request: UserFavoriteItemRequest, user: User):
    item_id = await item_service.get_item_id_by_item_name(user_favorite_item_request.item_name)
    user_favorite_item = UserFavoriteItem(user_id=user.id,
                                          item_id=item_id)
    exist_user_favorite_item = await check_if_user_favorite_item_exist(user_favorite_item)
    if exist_user_favorite_item:
        await user_favorite_item_repository.delete_user_favorite_item(user_favorite_item)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Can't delete {user_favorite_item_request.item_name} ,item not in favorite items list"
        )


async def delete_all_user_favorite_items(user: User):
    await user_favorite_item_repository.delete_all_user_favorite_items(user.id)
