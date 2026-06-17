import streamlit as st
from .components import show_header, show_error
from src.agents import process_query, summarize_articles, generate_situation_report
from src.tools import fetch_from_newsapi, fetch_from_gnews, fetch_from_rss
from src.memory import news_store

def show_input_page():
    show_header()
    show_error()
    
    st.text_input(
        "What topic do you want news about?", 
        placeholder="e.g. artificial intelligence, Pakistan cricket, Ukraine war, Gaza conflict, climate change...",
        key="topic_input"
    )
    
    st.number_input(
        "How many days back to search? (1–14)", 
        min_value=1, 
        max_value=14, 
        key="day_count"
    )
    
    disable_btn = not st.session_state.get("topic_input", "").strip()
    
    if st.button("Generate Situation Report", type="primary", disabled=disable_btn, use_container_width=True):
        topic = st.session_state["topic_input"].strip()
        days = st.session_state["day_count"]
        query_string = f"Show me {topic} news from the last {days} days"
        
        with st.spinner("Collecting and analyzing live news — this may take 30–60 seconds..."):
            try:
                # Run full pipeline
                parsed_params = process_query(query_string)
                keywords = parsed_params.get("keywords", [])
                start_date = parsed_params.get("start_date", "")
                end_date = parsed_params.get("end_date", "")
                
                count_per_source = 5
                arts_newsapi = fetch_from_newsapi(keywords, start_date, end_date, count_per_source)
                arts_gnews = fetch_from_gnews(keywords, start_date, end_date, count_per_source)
                arts_rss = fetch_from_rss(keywords, start_date, count_per_source)
                
                all_articles = arts_newsapi + arts_gnews + arts_rss
                unique_urls = set()
                deduped = []
                for a in all_articles:
                    u = a.get("url")
                    if u and u not in unique_urls:
                        unique_urls.add(u)
                        deduped.append(a)
                        
                summarized = summarize_articles(deduped)
                
                report_topic = parsed_params.get("topic", topic)
                report = generate_situation_report(summarized, report_topic, start_date, end_date)
                
                # Save to state and store
                st.session_state["results"] = report
                st.session_state["query_params"] = parsed_params
                st.session_state["error"] = None
                st.session_state["stage"] = "results"
                news_store.save_results(report)
                
                st.rerun()
            except Exception as e:
                st.session_state["error"] = f"Pipeline failed: {str(e)}"
                st.rerun()
                
    st.caption("Fetches live news from 3+ sources for any topic you enter.")