import streamlit as st
import pandas as pd
import os
from app import chat_page

st.title("Welcome to Lotus DA Hub!")

# DATA_SOURCE_OPTIONS = [
#     "Upload from your device",
#     "Use our sample dataset"
# ]
# source = st.radio(
#     label="Choose your data source",
#     options=DATA_SOURCE_OPTIONS,
#     index=None,
#     label_visibility="hidden"
# )

file = st.file_uploader(label="Upload your data",
                        accept_multiple_files=False,
                        type=["xlsx", "csv"])

# result = st.checkbox("Use our dataset :vv")

if file:
    st.session_state["uploaded_file"] = file
    file_extension = file.type.split("/")[-1]

    if file_extension == "csv":
        df = pd.read_csv(file)
    elif file_extension == 'xlsx':
        df = pd.read_excel(file, engine='openpyxl')

    st.session_state.data_frame = df

    st.dataframe(df)
    st.success("✅ Your dataset is loaded successfully!")
    st.info("You can navigate to `Play ground` tab to use our agent")
    st.page_link(chat_page)
