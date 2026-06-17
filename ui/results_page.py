import streamlit as st
from .components import show_header, show_error, show_source_badges
from src.memory import news_store

def show_results_page():
    show_header()
    show_error()
    
    col1, col2 = st.columns([3, 1])
    col1.subheader("Situation Report")
    if col2.button("New Search"):
        news_store.clear_results()
        st.session_state["stage"] = "input"
        st.session_state["query_params"] = None
        st.session_state["results"] = None
        st.session_state["error"] = None
        st.session_state["topic_input"] = ""
        st.session_state["day_count"] = 7
        st.rerun()
        
    results = st.session_state.get("results")
    if not results:
        st.warning("No results found.")
        return
        
    st.info(results.get("situation_overview", "No overview available."))
    
    st.write(f"**Period:** {results.get('period', '')} | **Topic:** {results.get('topic', '')}")
    
    st.subheader("Top Headlines")
    for i, h in enumerate(results.get("top_headlines", []), 1):
        st.write(f"{i}. {h}")
        
    st.subheader("Major Themes")
    for theme in results.get("major_themes", []):
        with st.expander(theme.get("theme", "Unknown Theme")):
            st.write(theme.get("description", ""))
            st.write("**Related Headlines:**")
            for rh in theme.get("related_headlines", []):
                st.write(f"- {rh}")
                
    st.subheader("Key Developments")
    for i, dev in enumerate(results.get("key_developments", []), 1):
        st.write(f"{i}. {dev}")
        
    st.subheader("Outlook")
    st.warning(results.get("outlook", "No outlook available."))
    
    st.subheader("Sources")
    show_source_badges(results.get("sources_cited", []))
    
    st.caption("Powered by GPT-4o · NewsAPI · GNews · RSS Feeds")