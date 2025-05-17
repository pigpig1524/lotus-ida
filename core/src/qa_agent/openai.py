import streamlit as st

from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import pandas as pd
import streamlit as st
import toml
import pandas as pd
from core.config import Config
from matplotlib import pyplot as plt
import contextlib
import re
import io


from langchain_experimental.agents.agent_toolkits import (
    create_pandas_dataframe_agent,
    create_csv_agent,
)


CSV_PROMPT_PREFIX = """
First set the pandas display options to show all the columns,
get the column names, then answer the question.
When you need to run Python code, use this exact format—without any brackets around the tool name:
Action: python_repl_ast
Action Input: <your Python command here>
"""

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
"""


MODEL = ChatOpenAI(api_key=Config.OPENAI_API_KEY,
                   model='gpt-4o-mini')

class OpenAIAgent:
    def __init__(self, data):
        self.client = create_pandas_dataframe_agent(llm=MODEL,
                                                    df=data,
                                                    verbose=True,
                                                    allow_dangerous_code=True)
        
    def run(self, user_input):
        try:
            response = self.client.invoke(CSV_PROMPT_PREFIX + user_input + CSV_PROMPT_SUFFIX)
            return response['output']
        except Exception as e:
            return "Something went wrong when we process your request! Please try again!"