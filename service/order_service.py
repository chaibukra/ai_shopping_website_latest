import datetime
import json
from typing import List, Optional
from fastapi import HTTPException
from starlette import status
from model.item_order import ItemOrder
from model.item_order_request import ItemOrderRequest
from model.order import Order
from model.order_request import OrderRequest
from model.order_response import OrderResponse
from model.order_status import OrderStatus
from model.user import User
from repository import order_repository, item_order_repository
from service import item_service


async def get_exist_temp_order(user_id: int) -> Optional[Order]:
    return await order_repository.exist_temp_order(user_id)


async def check_if_item_already_in_order(order_id, item_id) -> bool:
    return await item_order_repository.check_if_item_already_in_order(order_id, item_id)


async def temp_order_create_and_add_items(order_request: OrderRequest, user: User):
    item = await item_service.get_item_by_id(order_request.item_id)

    if item.quantity < order_request.item_quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The requested quantity is not available in stock. We have just {item.quantity} units in the stock, Please adjust the quantity for the order."
        )

    exist_temp_order = await get_exist_temp_order(user.id)

    if exist_temp_order is None:
        user_address = json.loads(user.address)
        city = user_address["city"]
        country = user_address["country"]
        order = Order(
            user_id=user.id,
            order_date=datetime.datetime.now(datetime.UTC).date(),
            shipping_address=f"{city}, {country}",
            order_status=OrderStatus.TEMP
        )
        order_id = await order_repository.create_order(order)

    else:
        order_id = exist_temp_order.order_id
        if await check_if_item_already_in_order(order_id, order_request.item_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provided item has already been added to the temp order item list"
            )

    item_order = ItemOrder(
        order_id=order_id,
        item_id=order_request.item_id,
        item_quantity=order_request.item_quantity)
    await item_order_repository.create_item_order(item_order)


async def update_quantity_item_in_temp_order(item_order_request: ItemOrderRequest, user):
    item = await item_service.get_item_by_id(item_order_request.item_id)
    if item.quantity < item_order_request.item_quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The requested quantity is not available in stock. We have just {item.quantity} units of {item.item_name}'s in stock, Please adjust the quantity for the order."
        )
    exist_temp_order = await get_exist_temp_order(user.id)
    item_in_order = await check_if_item_already_in_order(order_id=exist_temp_order.order_id, item_id=item_order_request.item_id)
    if item_in_order:
        item_order = ItemOrder(order_id=exist_temp_order.order_id, item_id=item_order_request.item_id,
                               item_quantity=item_order_request.item_quantity)
        await item_order_repository.update_item_order_quantity(item_order)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="item not in temp order")


async def close_order(user: User, shipping_address: str):
    exist_temp_order = await get_exist_temp_order(user.id)
    items_in_order = await item_order_repository.get_all_items_in_order(exist_temp_order.order_id)
    if items_in_order is not None:
        for item in items_in_order:
            await item_service.update_item_quantity_after_purchase(item.item_id, item.item_quantity)
        await order_repository.close_order(exist_temp_order.order_id, shipping_address)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not items in order")


async def del_empty_temp_order(temp_order_id):
    await order_repository.del_empty_temp_order(temp_order_id)


async def get_temp_order(user: User) -> Optional[OrderResponse]:
    exist_temp_order = await get_exist_temp_order(user.id)
    if exist_temp_order:
        items = await item_order_repository.get_all_items_in_order_with_full_details(exist_temp_order.order_id)
        if items is not None:
            items_price = 0
            for item in items:
                items_price += (item.price * item.quantity)
            temp_order = OrderResponse(items=items,
                                       shipping_address=exist_temp_order.shipping_address,
                                       order_total_price=items_price)
            return temp_order
        else:
            await del_empty_temp_order(exist_temp_order.order_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="The Cart Is Empty Now")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Your Cart Is Empty")


async def del_item_from_temp_order(item_id: int, user: User):
    exist_temp_order = await get_exist_temp_order(user.id)
    if exist_temp_order is not None:
        if await check_if_item_already_in_order(exist_temp_order.order_id, item_id):
            await item_order_repository.del_item_from_temp_order(exist_temp_order.order_id, item_id)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Can't Delete item ,The item not in The Temp Order")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't Delete item , Temp Order Not Found")


async def get_all_closed_order(user: User) -> List[OrderResponse]:
    all_closed_order = []
    closed_orders = await order_repository.get_closed_orders_ids(user.id)
    if closed_orders is not None:
        for order in closed_orders:
            items = await item_order_repository.get_all_items_in_order_with_full_details(order.order_id)
            items_price = 0
            for item in items:
                items_price += (item.price * item.quantity)
            closed_order = OrderResponse(items=items,
                                         shipping_address=order.shipping_address,
                                         order_total_price=items_price)
            all_closed_order.append(closed_order)
        return all_closed_order
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Close order not found")


async def delete_all_user_orders(user: User):
    all_orders_ids = await order_repository.get_all_orders_ids(user.id)
    await item_order_repository.delete_all_user_item_orders(all_orders_ids)
    await order_repository.delete_all_user_orders(user.id)


async def get_avg_total_quantity_for_closed_orders(user_id: int) -> Optional[int]:
    avg_total_quantity = await order_repository.get_avg_total_quantity_for_closed_orders(user_id)
    if avg_total_quantity is not None:
        return avg_total_quantity
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user id: {user_id} has not made any purchases so far")
