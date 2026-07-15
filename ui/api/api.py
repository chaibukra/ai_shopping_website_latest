import time
import requests
import streamlit as st
from starlette import status
from model.order_request import OrderRequest
from model.user_request import UserRequest
from model.user_favorite_item_request import UserFavoriteItemRequest
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

BASE_URL = os.getenv("BASE_URL")


def get_all_items():
    url = f"{BASE_URL}/item/"
    response = requests.get(url)
    return response.json()


def search_by_contain_name(words: str):
    url = f"{BASE_URL}/item/items_contain_words"
    params = {"words_to_search": words}
    response = requests.get(url, params=params)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")
        return None


def search_by_quantity(way_to_check: str, number: int):
    url = f"{BASE_URL}/item/items_by_amount"
    params = {"way_to_check": way_to_check, "number": number}
    response = requests.get(url, params=params)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")
        return None


def register_user(user: UserRequest):
    url = f"{BASE_URL}/user/"
    payload = {**user.dict()}
    payload["gender"] = payload["gender"].value
    response = requests.post(url, json=payload)
    if response.status_code == status.HTTP_201_CREATED:
        st.success(f"{user.username} Successfully Created")
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def get_token(username, password):
    url = f"{BASE_URL}/auth/token"
    form_data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, data=form_data)
    if response.status_code == status.HTTP_200_OK:
        st.session_state.refresh_token = response.json().get("jwt_refresh_token")
        st.session_state.access_token_expires_at = time.time() + response.json().get("expires_in")
        return response.json().get("jwt_token")
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")
        return None


def refresh_tokens():
    url = f"{BASE_URL}/auth/refresh"
    payload = {"refresh_token": st.session_state.refresh_token}
    response = requests.post(url, json=payload)
    if response.status_code == status.HTTP_200_OK:
        data = response.json()

        st.session_state.token = data.get("jwt_token")
        st.session_state.refresh_token = data.get("jwt_refresh_token")
        st.session_state.access_token_expires_at = time.time() + data.get("expires_in")
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def logout():
    url = f"{BASE_URL}/auth/logout"
    payload = {"refresh_token": st.session_state.refresh_token}
    response = requests.delete(url, json=payload)
    if response.status_code == status.HTTP_200_OK:
        st.session_state.token = None
        st.session_state.refresh_token = None
        st.session_state.access_token_expires_at = None
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def ensure_valid_access_token():
    if time.time() >= st.session_state.access_token_expires_at - 30:
        refresh_tokens()


def delete_user(username, password):
    url = f"{BASE_URL}/user/"
    form_data = {
        "username": username,
        "password": password
    }
    response = requests.delete(url, data=form_data)
    if response.status_code == status.HTTP_200_OK:
        st.success("User Successfully Deleted")
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")
        return None


def create_user_favorite_item(favorite_item: UserFavoriteItemRequest, token: str):
    ensure_valid_access_token()
    url = f"{BASE_URL}/user_favorite_item/"
    headers = {"Authorization": f"Bearer {token}"}
    payload = favorite_item.dict()
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == status.HTTP_201_CREATED:
        st.success(f"{favorite_item.item_name} Successfully Added To Your Favorite List")
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def get_favorite_items_list(token: str):
    ensure_valid_access_token()
    url = f"{BASE_URL}/user_favorite_item/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def delete_user_favorite_item(user_favorite_item_request: UserFavoriteItemRequest, token: str):
    ensure_valid_access_token()
    url = f"{BASE_URL}/user_favorite_item/"
    payload = user_favorite_item_request.dict()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers, json=payload)
    if response.status_code == status.HTTP_200_OK:
        st.success(f"{user_favorite_item_request.item_name} Successfully deleted")
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def update_item_quantity(item_order_request: dict, token: str):
    ensure_valid_access_token()
    url = f"{BASE_URL}/order/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(url, headers=headers, json=item_order_request)
    if response.status_code == status.HTTP_201_CREATED:
        st.success("Quantity Successfully Updated")
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def temp_order_create_and_add_items(order_request: OrderRequest, token: str):
    ensure_valid_access_token()
    url = f"{BASE_URL}/order/"
    payload = order_request.dict()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == status.HTTP_201_CREATED:
        st.success("Successfully Added")
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def close_order(token: str, shipping_address):
    ensure_valid_access_token()
    url = f"{BASE_URL}/order/close_order"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers, params={"shipping_address": shipping_address})
    if response.status_code == status.HTTP_200_OK:
        st.success("Order Successfully Closed")
        st.balloons()
        time.sleep(4)
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def get_temp_order(token: str):
    ensure_valid_access_token()
    url = f"{BASE_URL}/order/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def get_all_closed_order(token: str):
    ensure_valid_access_token()
    url = f"{BASE_URL}/order/get_all_closed_order"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def del_item_from_temp_order(item_id, token: str):
    ensure_valid_access_token()
    url = f"{BASE_URL}/order/del_item_from_temp_order"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers, params={"item_id": item_id})
    if response.status_code == status.HTTP_200_OK:
        st.success("Item Deleted Successfully from temp order")
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def get_user_role(token: str):
    ensure_valid_access_token()
    url = f"{BASE_URL}/user/role"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == status.HTTP_200_OK:
        return response.json().get("role")
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def get_all_users(token: str):
    ensure_valid_access_token()
    url = f"{BASE_URL}/user/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def predict_user_expenses_for_tech_items(user_id: int, token: str):
    ensure_valid_access_token()
    url = f"{BASE_URL}/predict/predict_user_expenses_for_tech_items"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"user_id": user_id}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        st.toast(response.json().get("detail"), icon=":material/error:")


def chat(session_id, chat_input):
    url = f"{BASE_URL}/chat/ask"
    response = requests.post(url, json={"session_id": session_id, "message": chat_input})
    full_message = response.json()["answer"]
    return full_message
