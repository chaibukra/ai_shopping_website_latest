import streamlit as st
import pandas as pd
from api import api
from background_config import set_png_as_page_bg

st.set_page_config(page_title="Your Orders", page_icon="🛒")

set_png_as_page_bg()


if "username" not in st.session_state:
    st.session_state.username = ""


def style_the_page():
    st.markdown(f"""
    <style>
    h1, h2, #hello-{st.session_state.username}-welcome-to-your-order-page {{
     text-align: center;
    }}
    
    h3 {{
     text-align: left;
    }}
    
    
    div.stNumberInput{{
      width: 30px;
      text-align: left;
    }}
    </style>
                """
                ,
                unsafe_allow_html=True)


style_the_page()

if "update_quantity" not in st.session_state:
    st.session_state.update_quantity = False

if "purchase" not in st.session_state:
    st.session_state.purchase = False


def update_change(product_name, product_id):
    api.update_item_quantity(
        {"item_id": product_id, "item_quantity": st.session_state["n" + product_name]},
        st.session_state.token)
    get_updated_temp_order_df()


def get_updated_temp_order_df():
    temp_order = api.get_temp_order(st.session_state.token)
    if temp_order:
        st.session_state.order_total_price = temp_order["order_total_price"]
        st.session_state.shipping_address = temp_order["shipping_address"]
        st.session_state.temp_order = {}
        for item in temp_order["items"]:
            st.session_state.temp_order[item["item_id"]] = item
    else:
        st.session_state.order_total_price = 0
        st.session_state.temp_order = {}


def get_updated_closed_order():
    st.session_state.closed_orders = api.get_all_closed_order(st.session_state.token)


if "token" not in st.session_state:
    st.session_state.token = None

st.title("Order Page")

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

if st.session_state.token is not None:
    get_updated_temp_order_df()

    if "closed_orders" not in st.session_state:
        get_updated_closed_order()

    st.subheader(f"Hello {st.session_state.username} Welcome To Your Order Page")
    # st.write("you can see allways your closed order in the end of the page")

    if st.session_state.temp_order is not None:
        st.header("Your Shopping Cart:")

        st.markdown("<div class='cart-container'>",
                    unsafe_allow_html=True)  # Start of the *outer* container
        for product_id, product in st.session_state.temp_order.items():
            st.markdown("<div class='cart-item'>",
                        unsafe_allow_html=True)  # Start of *inner* cart item container
            col1, col2 = st.columns([1, 3])

            with col1:
                st.image(product["image"], width=250)  # Product Image

            with col2:
                st.subheader(product["item_name"])

                st.number_input("quantity", value=product["quantity"],
                                key=f"n{product["item_name"]}",
                                on_change=update_change,
                                args=[product["item_name"], product["item_id"]])

                st.write(f"Price for unit : ${product['price']}")

                if st.button(f"🗑️️", key=f"order_remove_from_cart_{product['item_id']}", type="secondary"):
                    if st.session_state.token:
                        api.del_item_from_temp_order(product['item_id'], st.session_state.token)
                        get_updated_temp_order_df()
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)  # End of *inner* cart item container

        st.markdown("</div>", unsafe_allow_html=True)  # End of the *outer* container

        total_price = st.session_state.order_total_price
        st.write(f"Total Price: ${total_price:.2f}")
        if st.session_state.temp_order == {}:
            st.write("Your cart is empty.")
            if st.button("Go to see all items you can buy"):
                st.switch_page("Home.py")

        elif st.button("Purchase"):
            st.session_state.purchase = True

        if st.session_state.purchase:
            with st.form("Ship to"):
                st.subheader("Ship to")
                shipping_address = st.text_input("please enter shipping address for your order",
                                                 value=st.session_state.shipping_address)
                if st.form_submit_button("Done"):
                    if shipping_address:
                        st.session_state.purchase = False
                        api.close_order(st.session_state.token, shipping_address)
                        get_updated_temp_order_df()
                        get_updated_closed_order()
                        st.rerun()
                    else:
                        st.error("Please fill in all required fields.")

    if st.session_state.closed_orders is not None:
        st.header("Closed Orders", divider=True)
        for order in st.session_state.closed_orders:
            st.divider()
            st.write("Closed Order Details:")
            st.write(f"shipping address: {order.get("shipping_address")}")
            close_order = pd.DataFrame(order.get("items"), columns=["item_name", "price", "quantity"])
            st.dataframe(close_order)
            st.write(f"order total price: ${order.get("order_total_price"):.2f}")

else:
    st.header("Hello user please login to make order")
