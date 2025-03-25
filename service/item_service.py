from typing import List, Optional
from fastapi import HTTPException
from starlette import status
from model.item import Item
from repository import item_repository


async def get_item_by_id(item_id) -> Optional[Item]:
    item = await item_repository.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"The system not found any item with id: {item_id} in the database")
    return item


async def get_all_items() -> List[Item]:
    items = await item_repository.get_all_items()
    if not items:
        raise HTTPException(status_code=404, detail="The system not found any item in the database")
    return items


async def get_items_by_contain_name(words_to_search: str) -> Optional[List[Item]]:
    all_items = []
    words_list = words_to_search.split()
    for word in words_list:
        word = f"%{word}%"
        items = await item_repository.get_items_by_contain_name(word)
        if items:
            for item in items:
                if item not in all_items:
                    all_items.append(item)
    if not all_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The system not found any item in the database contain this words")
    else:
        return all_items


async def get_items_by_quantity(way_to_check: str, number: int) -> Optional[List[Item]]:
    items = await item_repository.get_items_by_quantity(way_to_check, number)
    if not items:
        raise HTTPException(status_code=404, detail="The system not found any item in the database")
    return items


async def get_item_id_by_item_name(item_name: str) -> Optional[int]:
    item = await item_repository.get_item_id_by_item_name(item_name)
    if not item:
        raise HTTPException(status_code=404, detail="The system not found any item with this name in the database")
    return item


async def update_item_quantity_after_purchase(item_id: int, quantity_to_decrease: int):
    await item_repository.update_item_quantity_after_purchase(item_id, quantity_to_decrease)
