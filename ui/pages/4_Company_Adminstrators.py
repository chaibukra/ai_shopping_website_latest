import streamlit as st
import pandas as pd
from api import api
from background_config import set_png_as_page_bg

st.set_page_config(page_title="Company Administrators", page_icon="🛒")

set_png_as_page_bg()

if "token" not in st.session_state:
    st.session_state.token = None

st.title("Company Administrators")

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
                    st.rerun()
    else:
        logout_btn = st.button("Logout")
        if logout_btn:
            st.session_state.token = None
            st.sidebar.success("Logout successfully")
            st.rerun()

if st.session_state.token is None:
    st.write("Please login")


role = api.get_user_role(st.session_state.token)

if role == "admin":
    st.header("Predict User Expense On Technology items")
    users = api.get_all_users(st.session_state.token)
    if users:
        df = pd.DataFrame(users, columns=["id", "username", "first_name", "last_name", "gender", "email", "role"])
        st.dataframe(df)
        user_id = st.text_input("Enter the user id you want to predict")
        if st.button("Submit"):
            if user_id.isdigit() and int(user_id) in df["id"].tolist():
                predict = api.predict_user_expenses_for_tech_items(user_id, st.session_state.token)
                st.dataframe(predict)
            else:
                st.error("Please Enter valid id")


else:
    st.error("only administrator authorize")
