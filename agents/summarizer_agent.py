import json
import re
import openai
from src.config import settings

def summarize_articles(articles: list) -> list:
    """Summarize a list of raw article dicts using GPT-4o."""
    if not articles:
        return []
        
    client = openai.OpenAI()
    
    system_instruction = (
        "You are a professional news summarizer for a real-time briefing system.\n"
        "You will receive a list of news articles.\n\n"
        "Return ONLY a raw JSON array with no markdown, no explanation, and no code fences.\n"
        "Each object in the array must have exactly these keys:\n"
        "- headline: string (clean headline under 15 words)\n"
        "- summary: string (exactly 2-3 sentences, factual only, no opinions)\n"
        "- key_entities: list of up to 5 people, organizations, or places mentioned\n"
        "- sentiment: one of \"positive\", \"negative\", \"neutral\"\n"
        "- category: string reflecting the actual topic of the article \n"
        "  (e.g. \"technology\", \"cricket\", \"climate\", \"conflict\" — \n"
        "  use whatever category fits, do not restrict to a fixed list)\n"
        "- citation: object with keys: source_name, url, published_at\n\n"
        "Rules:\n"
        "- Never fabricate details not present in the article text\n"
        "- Write in third person only\n"
        "- If the article text is too short to summarize meaningfully,\n"
        "  set summary to \"Insufficient content available.\"\n"
        "- Each citation must include the real source URL from the input"
    )

    user_content = json.dumps(articles, indent=2)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_content}
        ],
        temperature=0,
    )
    
    raw_content = response.choices[0].message.content

    # Strip any markdown/code fences that may appear accidentally
    cleaned = re.sub(r"^```\w*\n", "", raw_content)
    cleaned = re.sub(r"\n```$", "", cleaned)
    cleaned = cleaned.strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse JSON from summarizer response. Raw response: {raw_content}"
        ) from e

    print(f"Summarizer: {len(parsed)} articles summarized")
    return parsed
