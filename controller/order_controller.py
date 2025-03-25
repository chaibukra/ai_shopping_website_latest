from typing import Optional, List
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from exceptions.security_exceptions import user_unauthorized_exception
from model.item_order_request import ItemOrderRequest
from model.order_request import OrderRequest
from model.order_response import OrderResponse
from service import auth_service, order_service

router = APIRouter(prefix="/order",
                   tags=["order"])

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.put("/", status_code=status.HTTP_201_CREATED)
async def update_quantity_item_in_temp_order(item_order_request: ItemOrderRequest, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_token(token)
    if user is None:
        raise user_unauthorized_exception()
    await order_service.update_quantity_item_in_temp_order(item_order_request, user)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def temp_order_create_and_add_items(order_request: OrderRequest, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_token(token)
    if user is None:
        raise user_unauthorized_exception()
    await order_service.temp_order_create_and_add_items(order_request, user)


@router.post("/close_order")
async def close_order(shipping_address: str, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_token(token)
    if user is None:
        raise user_unauthorized_exception()
    await order_service.close_order(user, shipping_address)


@router.get("/")
async def get_temp_order(token: str = Depends(oauth2_bearer)) -> Optional[OrderResponse]:
    user = await auth_service.validate_token(token)
    if user is None:
        raise user_unauthorized_exception()
    return await order_service.get_temp_order(user)


@router.delete("/del_item_from_temp_order")
async def del_item_from_temp_order(item_id: int, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_token(token)
    if user is None:
        raise user_unauthorized_exception()
    return await order_service.del_item_from_temp_order(item_id, user)


@router.get("/get_all_closed_order")
async def get_all_closed_order(token: str = Depends(oauth2_bearer)) -> List[OrderResponse]:
    user = await auth_service.validate_token(token)
    if user is None:
        raise user_unauthorized_exception()
    return await order_service.get_all_closed_order(user)
