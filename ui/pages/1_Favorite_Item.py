import pandas as pd
import streamlit as st
from api import api
from model.user_favorite_item_request import UserFavoriteItemRequest
from background_config import set_png_as_page_bg

st.set_page_config(page_title="Your Favorite Items", page_icon="🛒")

set_png_as_page_bg()


def get_updated_favorite_list():
    favorite_item_df = api.get_favorite_items_list(st.session_state.token)
    df = pd.DataFrame(favorite_item_df, columns=["item_name", "price", "quantity"])
    st.session_state.favorite_item_df = df


if "token" not in st.session_state:
    st.session_state.token = None

if "counter" not in st.session_state:
    st.session_state.counter = 0
    items = api.get_all_items()
    st.session_state.items_df = pd.DataFrame(items, columns=['item_id', 'item_name', 'price', 'quantity'])

st.title("Favorite Item Page")

with st.sidebar.header("Login"):
    if st.session_state.token is None:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        col1, _, col2 = st.sidebar.columns([4, 3, 4])
        with col2:
            login_btn = st.button("Login")
            if login_btn:
                st.session_state.token = api.get_token(username, password)
                if st.session_state.token is not None:
                    st.sidebar.success("Login successfully")
                    st.session_state.username = username
                    if "favorite_item_df" in st.session_state:
                        del st.session_state["favorite_item_df"]
    else:
        logout_btn = st.button("Logout")
        if logout_btn:
            st.session_state.token = None
            st.sidebar.success("Logout successfully")

if st.session_state.token is not None:
    st.header(f"Hello {st.session_state.username} here you can see and modify your favorite items")
    selected_item = st.selectbox("Select an item", st.session_state.items_df['item_name'])
    col3, _, col4 = st.columns([4, 6.5, 5])
    with col3:
        if st.button("Add to my favorite list"):
            favorite_item = UserFavoriteItemRequest(item_name=selected_item)
            api.create_user_favorite_item(favorite_item, st.session_state.token)
            if "favorite_item_df" in st.session_state:
                del st.session_state["favorite_item_df"]
    with col4:
        if st.button("Delete from my favorite list"):
            favorite_item = UserFavoriteItemRequest(item_name=selected_item)
            api.delete_user_favorite_item(favorite_item, st.session_state.token)
            if "favorite_item_df" in st.session_state:
                del st.session_state["favorite_item_df"]
    with st.expander("My Favorite Item List"):
        if "favorite_item_df" not in st.session_state:
            get_updated_favorite_list()
        st.dataframe(st.session_state.favorite_item_df)

if st.session_state.token is None:
    st.header("Hello user please login for see and modify your favorite items")
