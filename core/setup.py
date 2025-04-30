import streamlit as st

def setup_session():
    if "uploaded_file" not in st.session_state:
        st.session_state["uploaded_file"] = None
    if "data_frame" not in st.session_state:
        st.session_state["data_frame"] = None

def setup_sidebar():
    st.logo("https://www.fit.hcmus.edu.vn/assets/img/logos/fit-logo.png")
    st.sidebar.title("Welcome to Lotus DA Hub!")