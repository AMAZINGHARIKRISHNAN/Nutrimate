import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import os

st.set_page_config(page_title="NutriMate", layout="wide")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles.css")

st.sidebar.title("Navigation")
page_selection = st.sidebar.radio("Go to", ["Nutrify","Meals Planner", "Tutorials", "Chatbot"])

if page_selection == "Nutrify":
    exec(open("Nutrition.py").read())

elif page_selection == "Meals Planner":
    exec(open("diet.py").read())

elif page_selection == "Tutorials":
    exec(open("Tutorials.py").read())

elif page_selection == "Chatbot":
    exec(open("Chatbot.py").read())

