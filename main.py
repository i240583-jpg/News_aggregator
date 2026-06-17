import os
import json
from dotenv import load_dotenv

# 1 & 2: Load and verify environment variables
load_dotenv()
required_keys = ["OPENAI_API_KEY", "NEWSAPI_KEY", "GNEWS_KEY"]
missing = [k for k in required_keys if not os.getenv(k)]
if missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

# 3 & 4: Import components
from src.agents import process_query, summarize_articles, generate_situation_report
from src.tools import fetch_from_newsapi, fetch_from_gnews, fetch_from_rss

def main():
    # 5: Hardcoded test query
    test_query = "Show me artificial intelligence news from the last 7 days"
    print(f"Starting pipeline with query: '{test_query}'\n")
    
    try:
        # Step A: Parse query
        parsed_params = process_query(test_query)
        print("Parsed parameters:", json.dumps(parsed_params, indent=2))
        
        keywords = parsed_params.get("keywords", [])
        start_date = parsed_params.get("start_date", "")
        end_date = parsed_params.get("end_date", "")
        
        # Step B: Fetch and deduplicate
        count_per_source = 5 # fetch up to 5 from each to keep it quick
        newsapi_arts = fetch_from_newsapi(keywords, start_date, end_date, count_per_source)
        gnews_arts = fetch_from_gnews(keywords, start_date, end_date, count_per_source)
        rss_arts = fetch_from_rss(keywords, start_date, count_per_source)
        
        all_articles = newsapi_arts + gnews_arts + rss_arts
        unique_urls = set()
        deduped_articles = []
        
        for art in all_articles:
            url = art.get("url")
            if url and url not in unique_urls:
                unique_urls.add(url)
                deduped_articles.append(art)
                
        print(f"\nTotal articles collected (after deduplication): {len(deduped_articles)}")
        
        # Step C: Summarize
        summarized = summarize_articles(deduped_articles)
        
        # Step D: Analyze
        topic = parsed_params.get("topic", "artificial intelligence")
        report = generate_situation_report(summarized, topic, start_date, end_date)
        
        print("\n--- SITUATION OVERVIEW ---")
        print(report.get("situation_overview", ""))
        print("\n--- TOP HEADLINES ---")
        for h in report.get("top_headlines", []):
            print(f"- {h}")
            
        print("\nPipeline complete.")
        
    except Exception as e:
        print(f"\nPipeline failed with error: {e}")

if __name__ == "__main__":
    main()