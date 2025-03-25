from typing import Optional, List
from fastapi import APIRouter
from model.item import Item
from service import item_service

router = APIRouter(
    prefix="/item",
    tags=["item"],
)


@router.get("/")
async def get_all_items() -> Optional[List[Item]]:
    return await item_service.get_all_items()


@router.get("/items_contain_words")
async def get_items_by_contain_name(words_to_search: str) -> Optional[List[Item]]:
    return await item_service.get_items_by_contain_name(words_to_search)


@router.get("/items_by_amount")
async def get_items_by_quantity(way_to_check: str, number: int) -> Optional[List[Item]]:
    return await item_service.get_items_by_quantity(way_to_check, number)


@router.get("/get_item_id_by_item_name/{item_name}")
async def get_item_id_by_item_name(item_name: str) -> Optional[int]:
    return await item_service.get_item_id_by_item_name(item_name)
