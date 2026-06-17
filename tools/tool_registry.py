import json
from .newsapi_tool import fetch_from_newsapi
from .gnews_tool import fetch_from_gnews
from .rss_tool import fetch_from_rss

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_news",
            "description": "Search for news articles using keywords, date range, and source type.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of keywords to search for"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of articles to fetch"
                    },
                    "source_type": {
                        "type": "string",
                        "enum": ["newsapi", "gnews", "rss", "all"],
                        "description": "The source to fetch news from."
                    }
                },
                "required": ["keywords", "start_date", "end_date", "count", "source_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_article_content",
            "description": "Fetch the full text content of an article given its URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the article to fetch"
                    }
                },
                "required": ["url"]
            }
        }
    }
]

def execute_tool(tool_name: str, args: dict) -> str:
    print(f"Tool called: {tool_name}")
    
    if tool_name == "search_news":
        keywords = args.get("keywords", [])
        start_date = args.get("start_date", "")
        end_date = args.get("end_date", "")
        count = args.get("count", 10)
        source_type = args.get("source_type", "all")
        
        results = []
        if source_type in ["newsapi", "all"]:
            results.extend(fetch_from_newsapi(keywords, start_date, end_date, count))
        if source_type in ["gnews", "all"]:
            results.extend(fetch_from_gnews(keywords, start_date, end_date, count))
        if source_type in ["rss", "all"]:
            results.extend(fetch_from_rss(keywords, start_date, count))
            
        return json.dumps(results)
        
    elif tool_name == "fetch_article_content":
        url = args.get("url", "")
        # Placeholder for actual scraping logic
        return f"Content for {url} would go here."
        
    else:
        return f"Error: Tool {tool_name} not recognized."