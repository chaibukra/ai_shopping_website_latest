import base64
import streamlit as st

image_path = r"ui/ai_website_picture.jpg"


@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_png_as_page_bg(png_file=image_path):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stHeading {
    width: 314px ;
    text-align: center;
    }
    .stButton {
    background-color: rgba(255, 255);
    color: black;
    padding: 10px;
    }

    .stFormSubmitButton {
    background-color: rgba(255, 255);
    color: black;
    padding: 10px;
    }
    .stSidebarUserContent {
    background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
    color: black;
    border: 1px solid black;
    padding: 2px;

    }

    .stError {
        color: red;
        font-weight: bold;
        margin-bottom: 10px;
    }


    .stSelectbox {
    background-color: white; /* Set background color to white */
    color: black; /* Set text color to black */
    border: 1px solid black; /* Add a border */
    padding: 10px;
}

    .stSlider {
    background-color: rgba(255, 255, 255, 0.8); 
    color: black;
    border: double;
    padding: 10px;
}
    .stTextInput {
    background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
    color: black;
    border: double;
    padding: 10px;}

    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: 80%%;
    background-position: center; /* Center the image */
    background-repeat: no-repeat;
    color: black; /* Set text color to black */
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); /* Add a text shadow */

    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

