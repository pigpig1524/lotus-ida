import streamlit as st
from pathlib import Path
import json
import os

class Config:
    OPENAI_API_KEY = st.secrets.get('OPENAI_API_KEY', None)
    UPSTAGE_API_KEY = st.secrets.get('UPSTAGE_API_KEY', None)
    GEMINI_API_KEY = st.secrets.get('GEMINI_API_KEY', None)
    CLASSIFICATIONS = {
        0: 'none',
        1: 'remove_duplicate_values',
        2: 'fill_missing_values',
        3: 'perform_dimensionality_reduction',
        4: 'perform_correlation_analysis',
    }
    # t = Path("core/src/context/system_prompt")
    # st.write(os.listdir(t))
    SYS_PROMPTS = {f.stem: f.read_text() for f in Path("core/src/context/system_prompt").glob("*.txt")}
    SYS_PROMPTS_CLASSIFICATION = SYS_PROMPTS['classification'].format(functions_dict=str(CLASSIFICATIONS))
    USER_PROMPTS = [f.read_text() for f in Path("core/src/context/user_prompt").glob("*.txt")]
    STRUCTURED_OUTPUT = {f.stem: json.load(f.open('r')) for f in Path("core/src/context/structured_output").glob("*.json")}