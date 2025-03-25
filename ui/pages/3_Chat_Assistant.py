import streamlit as st
import os
from google import genai
from google.genai import types
from api import api
from background_config import set_png_as_page_bg
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


st.set_page_config(page_title="Your AI Chat Assistant", page_icon="🛒")

set_png_as_page_bg()

if "df" not in st.session_state:
    st.session_state.df = api.get_all_items()

if "chat_massages" not in st.session_state:
    st.session_state.chat_massages = [
        {"name": "assistant", "content": "Hello I Am Your Assistant Today, What i can do for you?", "avatar": "👲"}]
    sys_instruct = f"You are a helpful helper to a shopping site. These are the details about the items in stock: {st.session_state.df}, the users can ask you what they want about the item, the questions can also be general questions that are not based on the stock, you must answer them but only if these items are in stock. Also, if the item quantity is 0 and the user asks something about that item, you should inform them that the item quantity is 0"

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    st.session_state.chat = client.chats.create(model="gemini-2.0-flash", config=types.GenerateContentConfig(
        temperature=1.5,
        system_instruction=sys_instruct))

if "massage_counter" not in st.session_state:
    st.session_state.massage_counter = 0

st.title("Chat Assistant")
st.header("Welcome to Our Ai Shopping Website")

for massage in st.session_state.chat_massages:
    st.chat_message(name=massage.get("name"), avatar=massage.get("avatar")).markdown(massage.get("content"))

chat_input = st.chat_input(placeholder="Please Enter your massage here")

if chat_input:
    if st.session_state.massage_counter != 5:
        st.session_state.chat_massages.append({"name": "user", "content": chat_input, "avatar": "😎"})

        stream = st.session_state.chat.send_message_stream(chat_input)

        with st.chat_message('user', avatar="😎"):
            st.markdown(chat_input)
        full_message = ""
        with st.chat_message('assistant', avatar="👲"):
            container = st.empty()
            for chunk in stream:
                full_message += chunk.text
                container.markdown(full_message)

        st.session_state.chat_massages.append(
            {"name": "assistant", "content": full_message, "avatar": "👲"})
        st.session_state.massage_counter += 1

    else:
        st.session_state.chat_massages.append(
            {"name": "assistant", "content": f"Sorry you have just 5 question you can ask", "avatar": "👲"})
        st.rerun()
