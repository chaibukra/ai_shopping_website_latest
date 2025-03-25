import json
from typing import List, Optional
from model.item import Item
from repository import cache_repository
from repository.database import database

TABLE_NAME = "item"


async def get_item_by_id(item_id: int) -> Optional[Item]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE item_id =:item_id"
    item = await database.fetch_one(query, values={"item_id": item_id})
    if item:
        return Item(**item)
    else:
        return None


async def get_all_items() -> List[Item]:
    if cache_repository.is_key_exists(TABLE_NAME):
        str_all_items = cache_repository.get_cache_entity(TABLE_NAME)
        all_items_data = json.loads(str_all_items)
        return [Item(**item) for item in all_items_data]
    else:
        query = f"SELECT * FROM {TABLE_NAME}"
        items = await database.fetch_all(query)
        all_items = [Item(**item) for item in items]
        cache_repository.create_cache_entity(TABLE_NAME, json.dumps([item.__dict__ for item in all_items]))
        return all_items


async def get_items_by_contain_name(word_to_search: str) -> Optional[List[Item]]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE item_name LIKE :word_to_search"
    items = await database.fetch_all(query, values={"word_to_search": word_to_search})
    if items:
        return [Item(**item) for item in items]
    else:
        return None


async def get_items_by_quantity(way_to_check: str, number: int) -> Optional[List[Item]]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE quantity {way_to_check} :number"
    items = await database.fetch_all(query, values={"number": number})
    if items:
        return [Item(**item) for item in items]
    else:
        return None


async def get_item_id_by_item_name(item_name: str) -> Optional[int]:
    query = f"SELECT item_id FROM {TABLE_NAME} WHERE item_name =:item_name"
    item = await database.fetch_one(query, values={"item_name": item_name})
    if item:
        return int(item[0])
    else:
        return None


async def update_item_quantity_after_purchase(item_id: int, quantity_to_decrease: int):
    query = f"""
    UPDATE {TABLE_NAME}
    SET quantity = quantity - :quantity_to_decrease
    WHERE item_id = :item_id
    """
    values = {"item_id": item_id, "quantity_to_decrease": quantity_to_decrease}
    if cache_repository.is_key_exists(TABLE_NAME):
        cache_repository.delete_cache_entity(TABLE_NAME)
    await database.execute(query, values=values)
