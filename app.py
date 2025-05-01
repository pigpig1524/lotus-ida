import streamlit as st
from core.setup import setup_session, setup_sidebar

setup_sidebar()
setup_session()

home_page = st.Page("pages/home.py", title="Home page", icon=":material/house:", default=True)
data_page = st.Page("pages/data.py", title="Data", icon=":material/description:")
chat_page = st.Page("pages/chat.py", title="Q&A Assistant", icon=":material/support_agent:")
data_process_page = st.Page("pages/data_process.py", title="Data process", icon=":material/manufacturing:")

pages = [home_page, data_page, data_process_page, chat_page]

page = st.navigation(pages)
page.run()