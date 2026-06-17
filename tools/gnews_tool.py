import os
import requests
from src.config import settings

def fetch_from_gnews(keywords: list, start_date: str, end_date: str, count: int) -> list:
    api_key = os.getenv("GNEWS_KEY")
    if not api_key or api_key == "your_gnews_key_here":
        print("Warning: valid GNEWS_KEY not found.")
        return []
        
    query = " OR ".join(keywords) if keywords else "news"
    url = "https://gnews.io/api/v4/search"
    # GNews uses ISO 8601 format or UTC.
    params = {
        "q": query,
        "apikey": api_key,
        "max": count,
        "lang": "en",
        "from": f"{start_date}T00:00:00Z",
        "to": f"{end_date}T23:59:59Z"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get("articles", [])
        if not articles:
            print("Warning: GNews returned no articles.")
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
            
        print(f"GNews: {len(clean_articles)} articles fetched")
        return clean_articles
        
    except Exception as e:
        print(f"Warning: GNews call failed - {e}")
        return []