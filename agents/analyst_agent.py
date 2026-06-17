import json
import re
import openai
from src.config import settings

def generate_situation_report(summaries: list, topic: str, start_date: str, end_date: str) -> dict:
    """Generate a structured situation report from summarized articles using GPT-4o."""
    client = openai.OpenAI()
    
    system_instruction = (
        "You are a senior intelligence analyst writing a structured situation report\n"
        "for a professional news briefing system.\n\n"
        "You will receive a list of summarized news stories for a given topic and date range.\n\n"
        "Return ONLY a raw JSON object with no markdown, no explanation, and no code fences.\n"
        "The object must have exactly these keys:\n"
        "- period: string (e.g. \"January 1–7, 2026\")\n"
        "- topic: string\n"
        "- total_sources: integer (number of unique sources in the input)\n"
        "- situation_overview: string (4-5 sentences giving the overall picture\n"
        "  of what happened. Write analytically, not journalistically.)\n"
        "- major_themes: list of objects, each with:\n"
        "    - theme: string (e.g. \"AI Regulation\", \"Trade Tensions\")\n"
        "    - description: string (2-3 sentences explaining the theme)\n"
        "    - related_headlines: list of headline strings from the input data\n"
        "- top_headlines: list of the 5 most important headline strings from the input\n"
        "- key_developments: list of exactly 5 strings, each describing one\n"
        "  important thing that happened during this period\n"
        "- outlook: string (2-3 sentences on what to watch next based on visible trends)\n"
        "- sources_cited: list of objects each with source_name and url\n\n"
        "Rules:\n"
        "- Base everything strictly on the summaries provided. No external knowledge.\n"
        "- Do not invent statistics, quotes, or events not present in the input.\n"
        "- If fewer than 3 articles are provided, set situation_overview to\n"
        "  \"Insufficient data to generate a situation report for this period and topic.\"\n"
        "- Always include sources_cited from the actual citation data in the input.\n"
        "- Write with analytical tone — concise, structured, professional."
    )

    user_content = json.dumps({
        "topic": topic,
        "date_range": f"{start_date} to {end_date}",
        "summaries": summaries
    }, indent=2)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_content}
        ],
        temperature=0,
    )
    
    raw_content = response.choices[0].message.content

    # Strip any markdown/code fences
    cleaned = re.sub(r"^```\w*\n", "", raw_content)
    cleaned = re.sub(r"\n```$", "", cleaned)
    cleaned = cleaned.strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse JSON from analyst response. Raw response: {raw_content}"
        ) from e

    print(f"Analyst: Situation report generated for {topic}")
    return parsed
