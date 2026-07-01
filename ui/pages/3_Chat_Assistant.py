import streamlit as st
from api import api
from background_config import set_png_as_page_bg
import uuid


st.set_page_config(page_title="Your AI Chat Assistant", page_icon="🛒")

set_png_as_page_bg()


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_massages" not in st.session_state:
    st.session_state.chat_massages = [
        {"name": "assistant", "content": "Hello I Am Your Assistant Today, What i can do for you?", "avatar": "👲"}]

if "massage_counter" not in st.session_state:
    st.session_state.massage_counter = 0

st.title("Chat Assistant")
st.header("Welcome to Our Ai Shopping Website")

for massage in st.session_state.chat_massages:
    st.chat_message(name=massage.get("name"), avatar=massage.get("avatar")).markdown(massage.get("content"))

chat_input = st.chat_input(placeholder="Please Enter your massage here")
if chat_input:
    if st.session_state.massage_counter != 40:

        st.session_state.chat_massages.append(
            {
                "name": "user",
                "content": chat_input,
                "avatar": "😎"
            }
        )

        with st.chat_message("user", avatar="😎"):
            st.markdown(chat_input)

        full_message = api.chat(st.session_state.session_id, chat_input)

        with st.chat_message("assistant", avatar="👲"):
            st.markdown(full_message)

        st.session_state.chat_massages.append(
            {
                "name": "assistant",
                "content": full_message,
                "avatar": "👲"
            }
        )

        st.session_state.massage_counter += 1

    else:
        st.session_state.chat_massages.append(
            {
                "name": "assistant",
                "content": "Sorry you have just 40 question you can ask",
                "avatar": "👲"
            }
        )
        st.rerun()