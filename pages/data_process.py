import streamlit as st
from core.src.helper import Helper

st.title("Data prcoess page")

if st.session_state.data_frame is None:
    st.warning("Please upload your data first")
else:
    helper = Helper(data=st.session_state.data_frame)
    user_input = st.chat_input("Tell me what you want to prcoess in this dataset...")
    if user_input:
        st.write(f"**User request**: {user_input}")
        response = helper.run(user_input)
        st.write(response)