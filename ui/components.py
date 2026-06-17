import streamlit as st

def show_header():
    st.title("News Situation Room")
    st.markdown("Live intelligence briefings from multiple sources.")
    st.divider()

def show_error():
    error = st.session_state.get("error")
    if error:
        st.error(error)
        if st.button("Dismiss"):
            st.session_state["error"] = None
            st.rerun()

def show_source_badges(sources_cited: list):
    if not sources_cited:
        return
        
    cols = st.columns(min(len(sources_cited), 6))
    for i, source in enumerate(sources_cited):
        name = source.get("source_name", "Unknown Source")
        url = source.get("url", "#")
        col = cols[i % len(cols)]
        col.markdown(f"[{name}]({url})")