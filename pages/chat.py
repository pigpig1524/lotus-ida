# import streamlit as st
# from openai import OpenAI
# from core.config import Config
# from core.src.helper import Helper


# def init_msg():
#     if "messages" not in st.session_state:
#         st.session_state.messages = [{'role': 'assistant', 'content': 'Hi! How can I assist you?'}]

# if st.session_state.data_frame is None:
#     st.warning("Please upload your data first")
# else:
#     st.session_state
#     helper = Helper(data=st.session_state.data_frame)

#     if 'message' not in st.session_state:
#         init_msg()

#     # Display chat messages from history on app rerun
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     if user_input := st.chat_input("Your message:"):
#         # Display user message in chat message container

#         with st.chat_message("user"):
#             st.markdown(user_input)
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": user_input})

#         response = helper.run(user_input)
#         # Display assistant response in chat message container
#         with st.chat_message("assistant"):
#             # st.write_stream(response)
#             st.markdown(response)
#         # Add assistant response to chat history
#         st.session_state.messages.append({"role": "assistant", "content": response})


import streamlit as st
from openai import OpenAI
from core.config import Config
from core.src.chat_agent import QAAgent


def init_msg():
    if "messages" not in st.session_state:
        st.session_state.messages = [{'role': 'assistant', 'content': 'Hi! How can I assist you?'}]

if st.session_state.data_frame is None:
    st.warning("Please upload your data first")
else:
    helper = QAAgent(data=st.session_state.data_frame)

    if 'message' not in st.session_state:
        init_msg()

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Your message:"):
        # Display user message in chat message container

        with st.chat_message("user"):
            st.markdown(user_input)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        response = helper.run(user_input)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            # st.write_stream(response)
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
