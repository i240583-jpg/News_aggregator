import streamlit as st
from src.ui.input_page import show_input_page
from src.ui.results_page import show_results_page

st.set_page_config(page_title="News Situation Room", page_icon="📰", layout="centered")

def init_session_state():
    defaults = {
        "stage": "input",
        "query_params": None,
        "results": None,
        "error": None,
        "topic_input": "",
        "day_count": 7
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def main():
    init_session_state()
    
    if st.session_state["stage"] == "input":
        show_input_page()
    elif st.session_state["stage"] == "results":
        show_results_page()

if __name__ == "__main__":
    main()