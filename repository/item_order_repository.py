from typing import Optional, List
from model.item import Item
from model.item_order import ItemOrder
from repository.database import database

TABLE_NAME = "item_order"
ITEM_TABLE_NAME = "item"


async def create_item_order(item_order: ItemOrder):
    query = f"""
    INSERT INTO {TABLE_NAME} (order_id, item_id, item_quantity)
    VALUES (:order_id, :item_id, :item_quantity)
    """
    values = {"order_id": item_order.order_id,
              "item_id": item_order.item_id,
              "item_quantity": item_order.item_quantity
              }
    await database.execute(query, values)


async def update_item_order_quantity(item_order: ItemOrder):
    query = f"""
    UPDATE {TABLE_NAME}
    SET item_quantity = :item_quantity
    WHERE order_id = :order_id
    AND
    item_id = :item_id
    """
    values = {"item_quantity": item_order.item_quantity,
              "order_id": item_order.order_id,
              "item_id": item_order.item_id
              }
    await database.execute(query, values)


async def check_if_item_already_in_order(order_id, item_id) -> bool:
    query = f"""
    SELECT *
    FROM {TABLE_NAME}
    WHERE item_id =:item_id
    AND order_id =:order_id
    """
    item = await database.fetch_one(query, values={"order_id": order_id, "item_id": item_id})
    if item:
        return True
    else:
        return False


async def get_all_items_in_order(order_id) -> Optional[List[ItemOrder]]:
    query = f"""
    SELECT *
    FROM {TABLE_NAME}
    WHERE order_id =:order_id
    """
    items_in_order = await database.fetch_all(query, values={"order_id": order_id})
    if items_in_order:
        return items_in_order
    else:
        return None


async def get_all_items_in_order_with_full_details(order_id) -> Optional[List[Item]]:
    query = f"""
    SELECT io.item_id, item_name, price ,item_quantity, image
    FROM {TABLE_NAME} io
    JOIN {ITEM_TABLE_NAME} it
    ON io.item_id = it.item_id
    WHERE order_id = :order_id
    """
    items_in_order = await database.fetch_all(query, values={"order_id": order_id})
    if items_in_order:
        return [Item(item_id=item.item_id, item_name=item.item_name, price=item.price, quantity=item.item_quantity, image=item.image)
                for item in items_in_order]
    else:
        return None


async def del_item_from_temp_order(order_id: int, item_id: int):
    query = f"""
    DELETE FROM {TABLE_NAME}
    WHERE order_id = :order_id AND item_id = :item_id
    """
    values = {"order_id": order_id, "item_id": item_id}
    await database.execute(query, values)


async def delete_all_user_item_orders(orders_ids):
    query = f"""
    DELETE FROM {TABLE_NAME}
    WHERE order_id in :orders_ids
    """
    values = {"orders_ids": orders_ids}
    await database.execute(query, values)
