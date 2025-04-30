import streamlit as st
from core.setup import setup_session, setup_sidebar

setup_sidebar()
setup_session()

home_page = st.Page("pages/home.py", title="Home page", icon=":material/house:", default=True)
data_page = st.Page("pages/data.py", title="Data", icon=":material/description:")
chat_page = st.Page("pages/chat.py", title="Play ground", icon=":material/support_agent:")

pages = [home_page, data_page, chat_page]

page = st.navigation(pages)
page.run()