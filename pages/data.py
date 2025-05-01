import streamlit as st
import pandas as pd
import os
from app import chat_page

st.title("Upload your data")

st.header("Choose a data source")
DATA_SOURCE_OPTIONS = [
    "Upload from your device",
    "Use our sample dataset"
]
source = st.radio(
    label="Choose your data source",
    options=DATA_SOURCE_OPTIONS,
    index=None,
    label_visibility="hidden"
)

if source == "Use our sample dataset":
    df = pd.read_csv('core/data/train.csv')
    st.session_state.data_frame = df
elif source == "Upload from your device":
    file = st.file_uploader(label="Upload your data",
                            accept_multiple_files=False,
                            type=["xlsx", "csv"],
                            key="uploader")

    if file:
        st.session_state["uploaded_file"] = file
        file_extension = file.type.split("/")[-1]

        if file_extension == "csv":
            df = pd.read_csv(file)
        elif file_extension == 'xlsx':
            df = pd.read_excel(file, engine='openpyxl')

        st.session_state.data_frame = df

        # st.dataframe(df)
        st.success("✅ Your dataset is loaded successfully!")
        st.info("You can navigate to `Play ground` tab to use our agent")
        # st.page_link(chat_page)

if st.session_state.data_frame is not None:
    st.header("Current working dataset")
    st.dataframe(st.session_state.data_frame)
