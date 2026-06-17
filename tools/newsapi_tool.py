import os
import requests
from src.config import settings

def fetch_from_newsapi(keywords: list, start_date: str, end_date: str, count: int) -> list:
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key or api_key == "your_newsapi_key_here":
        print("Warning: valid NEWSAPI_KEY not found.")
        return []
        
    query = " OR ".join(keywords) if keywords else "news"
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": start_date,
        "to": end_date,
        "pageSize": count,
        "apiKey": api_key,
        "language": "en",
        "sortBy": "publishedAt"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get("articles", [])
        if not articles:
            print("Warning: NewsAPI returned no articles.")
            return []
            
        clean_articles = []
        for a in articles:
            clean_articles.append({
                "title": a.get("title", ""),
                "source": a.get("source", {}).get("name", "Unknown"),
                "url": a.get("url", ""),
                "published_at": a.get("publishedAt", ""),
                "description": a.get("description", "")
            })
            
        print(f"NewsAPI: {len(clean_articles)} articles fetched")
        return clean_articles
        
    except Exception as e:
        print(f"Warning: NewsAPI call failed - {e}")
        return []