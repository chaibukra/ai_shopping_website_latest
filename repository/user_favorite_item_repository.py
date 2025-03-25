from typing import List, Optional
from model.user_favorite_item import UserFavoriteItem
from model.user_favorite_item_response import UserFavoriteItemResponse
from repository.database import database

TABLE_NAME = "user_favorite_item"
ITEM_TABLE_NAME = "item"


async def create_user_favorite_item(user_favorite_item: UserFavoriteItem):
    query = f""" 
    INSERT INTO {TABLE_NAME} (user_id, item_id)
    VALUES (:user_id, :item_id)
    """
    values = {"user_id": user_favorite_item.user_id, "item_id": user_favorite_item.item_id}
    await database.execute(query, values)


async def check_if_user_favorite_item_exist(user_favorite_item: UserFavoriteItem) -> bool:
    query = f""" 
    SELECT * FROM {TABLE_NAME} WHERE user_id =:user_id AND item_id =:item_id
    """
    values = {"user_id": user_favorite_item.user_id, "item_id": user_favorite_item.item_id}
    exist_user_favorite_item = await database.fetch_one(query, values)
    if exist_user_favorite_item:
        return True
    else:
        return False


async def get_favorite_items_list(user_id) -> Optional[List[UserFavoriteItemResponse]]:
    query = f"""
    SELECT item_name, price, quantity
    FROM {TABLE_NAME} favorite
    JOIN {ITEM_TABLE_NAME}
    ON favorite.item_id = item.item_id
    WHERE user_id =:user_id
    """
    favorite_items_list = await database.fetch_all(query, values={"user_id": user_id})
    if favorite_items_list:
        return favorite_items_list
    else:
        return None


async def delete_user_favorite_item(user_favorite_item: UserFavoriteItem):
    query = f"""
    DELETE FROM {TABLE_NAME}
    WHERE user_id =:user_id
    AND item_id =:item_id
    """
    values = {"user_id": user_favorite_item.user_id, "item_id": user_favorite_item.item_id}
    await database.execute(query, values=values)


async def delete_all_user_favorite_items(user_id: int):
    query = f"""
    DELETE FROM {TABLE_NAME}
    WHERE user_id =:user_id
    """
    await database.execute(query, values={"user_id": user_id})
