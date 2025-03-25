import streamlit as st
from email_validator import EmailNotValidError, validate_email
from api import api
from model.user_request import UserRequest
from model.user_gender import UserGender
from model.order_request import OrderRequest
from model.user_favorite_item_request import UserFavoriteItemRequest
from background_config import set_png_as_page_bg

st.set_page_config(page_title="Chai Bukra Store", page_icon="🛒")

set_png_as_page_bg()

st.title("AI Shopping Website")
st.header("Welcome to Our Ai Shopping Website")
st.write("Welcome to our app! Use the sidebar to navigate between pages.")


def get_updated_temp_order_df():
    cart = api.get_temp_order(st.session_state.token)
    if cart:
        st.session_state.order_total_price = cart["order_total_price"]
        st.session_state.cart = {}
        for item in cart["items"]:
            st.session_state.cart[item["item_id"]] = item
    else:
        st.session_state.order_total_price = 0
        st.session_state.cart = {}


def get_updated_favorite_items():
    favorite_items = api.get_favorite_items_list(st.session_state.token)
    if favorite_items:
        st.session_state.favorite_items = {}
        for item in favorite_items:
            st.session_state.favorite_items[item["item_name"]] = item
    else:
        st.session_state.favorite_items = {}


if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token is not None:
    get_updated_temp_order_df()
    get_updated_favorite_items()


# --- Shopping Cart (Session State) ---
if "cart" not in st.session_state:
    st.session_state.cart = {}  # Initialize an empty dictionary

if "favorite_items" not in st.session_state:
    st.session_state.favorite_items = {}

if "df" not in st.session_state:
    st.session_state.df = api.get_all_items()

if 'show_registration_form' not in st.session_state:
    st.session_state['show_registration_form'] = False

with st.sidebar.header("Login"):
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    col1, _, col2 = st.sidebar.columns([1, 0.1, 1])
    with col1:
        login_btn = st.button("Login")
        if login_btn:
            st.session_state.token = api.get_token(username, password)
            if st.session_state.token is not None:
                st.sidebar.success("Login successfully")
                st.session_state.username = username
                if "favorite_item_df" in st.session_state:
                    del st.session_state["favorite_item_df"]
                st.rerun()
    with col2:
        logout_btn = st.button("Logout")
        if logout_btn:
            st.session_state.token = None
            st.session_state.favorite_items = {}
            st.session_state.order_total_price = 0
            st.session_state.cart = {}
            st.sidebar.success("Logout successfully")
            st.rerun()

        delete_user = st.button("Delete User")
        if delete_user:
            api.delete_user(username, password)
            st.session_state.token = None
            st.session_state.favorite_items = {}
            st.session_state.order_total_price = 0
            st.session_state.cart = {}

    if st.button("New User"):
        st.session_state.show_registration_form = not st.session_state.show_registration_form
        if st.session_state.show_registration_form:
            st.write("Please fill out the registration form below")

col1, col2 = st.columns([8, 2])

with col1:
    search_bar = st.text_input("Search items")

with col2:
    search_button = st.button("Search")

if search_button:
    if search_bar:
        st.session_state.df = api.search_by_contain_name(search_bar)

col3, col4, col5 = st.columns([5, 2, 2])

with col3:
    slider = st.slider("Select Quantity", min_value=0, max_value=600, value=100, step=1)

with col4:
    way_to_search = st.selectbox("choose a the way to quantity search", options=[">", "<", "="], index=0)

with col5:
    quantity_search_button = st.button("Search by Quantity")

    rest_search_button = st.button("Show All Items")

if quantity_search_button:
    st.session_state.df = api.search_by_quantity(way_to_search, slider)

if rest_search_button:
    st.session_state.df = api.get_all_items()

# --- Display Products ---
st.title("Our Products")
if st.session_state.df:
    for product in st.session_state.df:
        st.markdown("<div class='product-container'>", unsafe_allow_html=True)  # Start product container
        col1, col2 = st.columns([1, 2])  # Image and Content columns

        with col1:
            st.image(product["image"], width=250)  # Product Image
        with col2:
            st.subheader(product["item_name"])
            st.write(f"quantity on stock: {product["quantity"]}")
            st.write(f"Price: {product['price']}")
            if product["item_id"] not in st.session_state.cart:
                if st.button(f"Add to Cart 🛒",
                             key=f"add_to_cart_{product['item_id']}"):
                    if st.session_state.token:
                        order = OrderRequest(item_id=product['item_id'], item_quantity=1)
                        api.temp_order_create_and_add_items(order, st.session_state.token)
                        st.rerun()
                    else:
                        st.write("Please login to add to cart")
            else:
                if st.button(f"Remove from Cart ❌",
                             key=f"remove_from_cart_{product['item_id']}"):
                    if st.session_state.token:
                        api.del_item_from_temp_order(product['item_id'], st.session_state.token)
                        st.rerun()
            if product["item_name"] not in st.session_state.favorite_items:
                if st.button("Add to my favorite list 🤍", key=f"add_favorite_{product['item_name']}"):
                    if st.session_state.token:
                        favorite_item = UserFavoriteItemRequest(item_name=product["item_name"])
                        api.create_user_favorite_item(favorite_item, st.session_state.token)
                    else:
                        st.write("Please login to add to Favorite")
            else:
                if st.button("Delete from my favorite list ⛔", key=f"delete_favorite_{product['item_name']}"):
                    favorite_item = UserFavoriteItemRequest(item_name=product['item_name'])
                    api.delete_user_favorite_item(favorite_item, st.session_state.token)

        st.markdown("</div>", unsafe_allow_html=True)  # Close product container

if st.session_state.show_registration_form:
    st.header("Register a New User")
    with st.form("Register Form"):
        username = st.text_input("Username", key="register_username")
        first_name = st.text_input("First Name", key="register_firstname")
        last_name = st.text_input("Last Name", key="register_lastname")
        gender = st.selectbox("Gender", [gender.value for gender in UserGender])
        age = st.text_input("Age", key="register_age")
        password = st.text_input("Password", type='password', key="register_password")
        email = st.text_input("Email", key="register_email")
        phone = st.text_input("Phone", key="register_phone")
        country = st.text_input("Country", key="register_country")
        city = st.text_input("City", key="register_city")

        register_btn = st.form_submit_button("Register")

    if register_btn:
        try:
            valid = validate_email(email)

        except EmailNotValidError as e:
            st.error(str(e))

        if not all([username, first_name, last_name, gender, age, password, email, phone, country, city]):
            st.error("Please fill in all required fields.")

        elif any(char.isdigit() for char in first_name):
            st.error("Please enter valid first name")

        elif any(char.isdigit() for char in last_name):
            st.error("Please enter valid last name")

        elif not age.isdigit() or int(age) < 1 or int(age) > 120:
            st.error("Please enter valid age")

        elif not phone.isdigit() or len(phone) != 10:
            st.error("please enter valid phone number")
        else:
            user_request = UserRequest(first_name=first_name,
                                       last_name=last_name,
                                       gender=gender,
                                       age=age,
                                       email=email,
                                       phone=phone,
                                       country=country,
                                       city=city,
                                       username=username,
                                       password=password)

            api.register_user(user_request)

# --- Display Cart ---
st.sidebar.title("Shopping Cart")

if st.session_state.cart:

    st.sidebar.markdown("<div class='cart-container'>", unsafe_allow_html=True)  # Start of the *outer* container

    for product_id, product in st.session_state.cart.items():
        st.sidebar.markdown("<div class='cart-item'>", unsafe_allow_html=True)  # Start of *inner* cart item container
        col1, col2 = st.sidebar.columns([1, 3])
        with col1:
            st.image(product["image"], width=50, caption=f"{product['price']}")  # Small product image

        with col2:
            if st.button(f"🗑️️", key=f"sidebar_remove_from_cart_{product['item_id']}", type="secondary"):
                if st.session_state.token:
                    api.del_item_from_temp_order(product['item_id'], st.session_state.token)
                st.rerun()
        st.sidebar.markdown("</div>", unsafe_allow_html=True)  # End of *inner* cart item container

    st.sidebar.markdown("</div>", unsafe_allow_html=True)  # End of the *outer* container

    total_price = st.session_state.order_total_price
    st.sidebar.write(f"Total: ${total_price:.2f}")

    if st.sidebar.button("Checkout"):
        st.switch_page("pages/2_Order.py")
else:
    st.sidebar.write("Your cart is empty.")
