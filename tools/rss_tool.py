import feedparser
from dateutil import parser as date_parser
from datetime import datetime, timezone

def fetch_from_rss(keywords: list, start_date: str, count: int) -> list:
    feeds = [
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://feeds.reuters.com/reuters/topNews",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "https://feeds.skynews.com/feeds/rss/world.xml"
    ]
    
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except Exception:
        start_dt = datetime.min.replace(tzinfo=timezone.utc)
        
    keywords_lower = [k.lower() for k in keywords]
    clean_articles = []
    
    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                
                # Check keywords
                match = False
                if not keywords:
                    match = True
                else:
                    match = any(kw.lower() in (title + summary).lower() for kw in keywords)
                            
                if not match:
                    continue
                    
                # Check date
                pub_date_str = entry.get("published", "")
                if pub_date_str:
                    try:
                        pub_dt = date_parser.parse(pub_date_str)
                        if pub_dt.tzinfo is None:
                            pub_dt = pub_dt.replace(tzinfo=timezone.utc)
                        if pub_dt < start_dt:
                            continue
                    except Exception:
                        pass # If we can't parse date, we keep it to be safe
                
                clean_articles.append({
                    "title": title,
                    "source": feed.feed.get("title", "RSS Feed"),
                    "url": entry.get("link", ""),
                    "published_at": pub_date_str,
                    "description": summary
                })
                
                if len(clean_articles) >= count:
                    print(f"RSS: {len(clean_articles)} articles fetched")
                    return clean_articles
                    
        except Exception as e:
            print(f"Warning: Failed to fetch from RSS feed {feed_url} - {e}")
            
    if not clean_articles:
        print("Warning: All RSS feeds failed or returned no matching articles.")
    else:
        print(f"RSS: {len(clean_articles)} articles fetched")
        
    return clean_articles[:count]