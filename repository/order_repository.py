from typing import Optional, List
from model.order import Order
from model.order_status import OrderStatus
from repository.database import database

TABLE_NAME = "orders"
ITEM_ORDER_TABLE_NAME = "item_order"

async def create_order(order: Order) -> int:
    query = f"""
    INSERT INTO {TABLE_NAME} (user_id, order_date, shipping_address, order_status)
    VALUES (:user_id, :order_date, :shipping_address, :order_status)
    """
    values = {
        "user_id": order.user_id,
        "order_date": order.order_date,
        "shipping_address": order.shipping_address,
        "order_status": order.order_status.value}

    async with database.transaction():
        await database.execute(query, values)
        order_id = await database.fetch_one("SELECT LAST_INSERT_ID()")

    return int(order_id[0])


async def exist_temp_order(user_id: int) -> Optional[Order]:
    query = f"""
    SELECT * FROM {TABLE_NAME} WHERE user_id =:user_id AND order_status = :order_status
    """
    values = {"user_id": user_id, "order_status": OrderStatus.TEMP.value}
    temp_order = await database.fetch_one(query, values)
    if temp_order:
        return Order(**temp_order)
    else:
        return None


async def close_order(order_id: int, shipping_address: str):
    query = f"""
    UPDATE  {TABLE_NAME} 
    SET order_status = :order_status , shipping_address = :shipping_address
    WHERE order_id = :order_id
    """
    values = {
        "order_status": OrderStatus.CLOSE.value,
        "shipping_address": shipping_address,
        "order_id": order_id,
    }

    await database.execute(query, values)


async def del_empty_temp_order(temp_order_id: int):
    query = f"""
    DELETE FROM {TABLE_NAME}
    WHERE order_id = :temp_order_id
    """
    values = {"temp_order_id": temp_order_id}
    await database.execute(query, values)


async def get_closed_orders_ids(user_id: int):
    query = f"""
     SELECT order_id, shipping_address FROM {TABLE_NAME} WHERE user_id =:user_id AND order_status = :order_status
     """
    values = {"user_id": user_id, "order_status": OrderStatus.CLOSE.value}
    closed_order_ids = await database.fetch_all(query, values)
    if closed_order_ids:
        return closed_order_ids
    else:
        return None


async def get_all_orders_ids(user_id: int):
    query = f"""
     SELECT order_id FROM {TABLE_NAME} WHERE user_id =:user_id
     """
    values = {"user_id": user_id}
    all_orders_ids = await database.fetch_all(query, values)
    if all_orders_ids:
        return [int(order[0]) for order in all_orders_ids]
    else:
        return None


async def delete_all_user_orders(user_id: int):
    query = f"""
    DELETE FROM {TABLE_NAME}
    WHERE user_id = :user_id
    """
    values = {"user_id": user_id}
    await database.execute(query, values)


async def get_avg_total_quantity_for_closed_orders(user_id: int) -> Optional[int]:
    query = f"""
    SELECT 
          AVG(total_quantity_per_order) AS avg_total_quantity_per_order 
    FROM 
    (
        SELECT 
            o.order_id, 
            SUM(io.item_quantity) AS total_quantity_per_order 
        FROM 
            {TABLE_NAME} o 
        JOIN 
            {ITEM_ORDER_TABLE_NAME} io ON o.order_id = io.order_id 
        WHERE 
            o.user_id = :user_id
            AND o.order_status  = :order_status
        GROUP BY 
            o.order_id
    ) AS subquery;
    """

    values = {"user_id": user_id, "order_status": OrderStatus.CLOSE.value}
    avg_total_quantity = await database.fetch_one(query, values)

    if avg_total_quantity[0]:
        return int(avg_total_quantity[0])
    else:
        return None


