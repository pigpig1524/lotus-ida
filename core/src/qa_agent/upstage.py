import streamlit as st
from langchain_upstage import ChatUpstage
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
import toml
import os
from langchain.schema.runnable import RunnableLambda

# st.set_page_config(page_title="CSV Solar Agent", layout="wide")

# --- API Key ---
# secrets = toml.load("./core/research/QA/.streamlit/secrets.toml")
# solar_api_key = secrets["api_keys"]["solar"]
# os.environ["UPSTAGE_API_KEY"] = solar_api_key
# secrets = toml.load("../../../.streamlit/secrets.toml")
# solar_api_key = secrets['UPSTAGE_API_KEY']
# os.environ["UPSTAGE_API_KEY"] = solar_api_key

SOLAR_API_KEY = st.secrets["UPSTAGE_API_KEY"]

@st.cache_resource
def get_solar_runnable():
    solar_llm = ChatUpstage(
        model="solar-pro",
        openai_api_base="https://api.upstage.ai/v1/solar",
        openai_api_key=SOLAR_API_KEY,
        streaming=False,
        max_tokens= 2024,    
        temperature= 0.0
    )
    return RunnableLambda(lambda inputs, **kwargs: solar_llm.invoke(inputs, **kwargs))

# solar_runnable = get_solar_runnable()

solar_runnable = ChatUpstage(
        model="solar-pro",
        openai_api_base="https://api.upstage.ai/v1/solar",
        openai_api_key=SOLAR_API_KEY,
        streaming=False,
        max_tokens= 2024,    
        temperature= 0.0
    )

CSV_PROMPT_PREFIX = """
First set the pandas display options to show all the columns,
get the column names, then answer the question.
When you need to run Python code, use this exact format—without any brackets around the tool name:
Action: python_repl_ast
Action Input: <your Python command here>
"""

# CSV_PROMPT_SUFFIX = """
# - **ALWAYS** before giving the Final Answer, try another method.
# - **DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE,
# ONLY USE THE RESULTS OF THE CALCULATIONS YOU HAVE DONE**.
# - **ALWAYS**, as part of your "Final Answer", explain how you got
# to the answer on a section that starts with: "\\n\\nExplanation:\\n".
# In the explanation, mention the column names that you used to get
# to the final answer.
# - Do not hallucinate or invent answers not in the data.
# """
CSV_PROMPT_SUFFIX = """
- **ALWAYS** before giving the Final Answer, try another method.
Then reflect on the answers of the two methods you did and ask yourself
if it answers correctly the original question.
If you are not sure, try another method.
FORMAT 4 FIGURES OR MORE WITH COMMAS.
- If the methods tried do not give the same result,reflect and
try again until you have two methods that have the same result.
- If you still cannot arrive to a consistent result, say that
you are not sure of the answer.
- If you are sure of the correct answer, create a beautiful
and thorough response using Markdown.
- **DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE,
ONLY USE THE RESULTS OF THE CALCULATIONS YOU HAVE DONE**.
- **ALWAYS**, as part of your "Final Answer", explain how you got
to the answer on a section that starts with: "\n\nExplanation:\n".
In the explanation, mention the column names that you used to get
to the final answer.
- If the user asks to visualize, plot, draw, chart, or show a graph:
    - DO generate the appropriate Python code using matplotlib.
    - DO include the code at the end of your "Final Answer" in Markdown response.
    - Wrap the code in a proper Python Markdown code block
"""

# # --- Streamlit App UI ---
# st.title("🔍 CSV Solar Agent")

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# st.sidebar.header("Upload CSV")
# uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# if uploaded_file:
#     if "df" not in st.session_state:
#         df = pd.read_csv(uploaded_file).fillna(0)
#         st.session_state.df = df
#         st.session_state.agent = create_pandas_dataframe_agent(
#             llm=solar_runnable,
#             df=df,
#             verbose=True,
#             agent_executor_kwargs={"handle_parsing_errors": True},
#             allow_dangerous_code=True,
#         )
#         st.success("✅ CSV loaded successfully.")
#     else:
#         df = st.session_state.df
#         agent = st.session_state.agent

#     col1, col2 = st.columns([1, 2])

#     with col1:
#         st.write("### 📊 CSV Preview")
#         st.dataframe(df, use_container_width=True)

#     with col2:
#         st.subheader("💬 Chat with the Dataset")

#         chat_placeholder = st.empty()

#         def render_chat():
#             html = "<div style='height:400px; overflow-y:auto; border:1px solid #ccc; padding:10px;'>"
#             for msg in st.session_state.chat_history:
#                 if msg["role"] == "user":
#                     html += f"<p style='text-align:right; color:#ffffff;'><b>You:</b> {msg['content']}</p>"
#                 else:
#                     html += f"<p style='text-align:left; color:#ffffff;'><b>Assistant:</b> {msg['content']}</p>"
#             html += "</div>"
#             chat_placeholder.markdown(html, unsafe_allow_html=True)

#         user_input = ""
#         user_input = st.chat_input("Ask a question about the dataset...")
        
        
#         if user_input:
#             st.session_state.chat_history.append({"role": "user", "content": user_input})
#             render_chat()

#             QUERY = CSV_PROMPT_PREFIX + user_input + CSV_PROMPT_SUFFIX
#             res = agent.invoke(QUERY)
#             reply = res["output"]

#             st.session_state.chat_history.append({"role": "assistant", "content": reply})
#             render_chat()


# else:
#     st.info("👈 Please upload a CSV file from the sidebar to start.")


class UpstageAgent:
    def __init__(self, data: pd.DataFrame):
        self.client = create_pandas_dataframe_agent(
            llm=solar_runnable,
            df=data,
            verbose=True,
            agent_executor_kwargs={"handle_parsing_errors": True},
            allow_dangerous_code=True,
        )

    def run(self, user_input: str):
        try:
            # response = self.client.invoke(CSV_PROMPT_PREFIX + user_input + CSV_PROMPT_SUFFIX)
            response = self.client.invoke(user_input)
            from pprint import pprint
            pprint(response)
            return response['output']
        except Exception as e:
            st.error(str(e))
            return "Something went wrong when we process your request! Please try again!"