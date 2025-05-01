import streamlit as st
from core.src.helper import Helper
import pandas as pd
import json

st.title("Data process page")

if st.session_state.data_frame is None:
    st.warning("Please upload your data first")
else:
    helper = Helper(data=st.session_state.data_frame)

    # Store user input in session_state
    user_input = st.chat_input("Tell me what you want to process in this dataset...")
    if user_input:
        st.session_state.last_input = user_input

    # Only run if we have something stored
    if "last_input" in st.session_state:
        st.write(f"**User request**: {st.session_state.last_input}")
        response, data = helper.run(st.session_state.last_input)

        if isinstance(data, pd.DataFrame):
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download the result",
                data=csv,
                file_name="data.csv",
                mime='text/csv'
            )
        elif isinstance(data, dict):
            json_data = pd.DataFrame(data)
            # json_data = json.dumps(data, indent=2).encode('utf-8')
            json_data = json_data.to_json(indent=2).encode('utf-8')
            st.download_button(
                "Download the result",
                data=json_data,
                file_name='result.json',
                mime='application/json'
            )
        st.write(response)
