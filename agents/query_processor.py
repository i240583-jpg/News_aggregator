import os
import json
import re
import datetime
import openai

# Import settings to ensure environment variables are loaded
from src.config import settings  # noqa: F401

def process_query(raw_input: str) -> dict:
    """Parse a raw user query into structured search parameters.

    This function uses the OpenAI GPT‑4o model with a system instruction that
    forces the model to return a single raw JSON object (no markdown, no code
    fences). The JSON contains ``topic``, ``start_date``, ``end_date``,
    ``keywords`` and ``region`` as specified in the prompt.

    Args:
        raw_input: The raw string entered by the user.

    Returns:
        A dictionary with the parsed parameters.

    Raises:
        ValueError: If the model response cannot be parsed as valid JSON.
    """
    # Initialise OpenAI client
    openai.api_key = os.getenv("OPENAI_API_KEY")

    today = datetime.date.today()
    system_instruction = (
        "You are a news query parser and keyword expansion engine.\n"
        "Extract search parameters from the user's input and return ONLY a raw JSON\n"
        "object with no markdown, no explanation, and no code fences.\n\n"
        "The JSON must contain these exact keys:\n"
        "- topic: string (whatever topic the user mentions, e.g. \"technology\",\n"
        "  \"cricket\", \"Iran US deal\", \"Gaza conflict\", \"Pakistan economy\".\n"
        "  Accept any topic without restriction. Use the user's exact words.)\n"
        "- start_date: string in YYYY-MM-DD format\n"
        "- end_date: string in YYYY-MM-DD format\n"
        "- keywords: list of 6-8 search keywords and phrases that a journalist\n"
        "  would use in a headline when writing about this topic.\n"
        "  This list must include:\n"
        "  * The original words the user typed\n"
        "  * Alternate names and synonyms for the main subjects\n"
        "  * Related proper nouns (country capitals, organization names, \n"
        "    leader names, acronyms)\n"
        "  * Related action words (e.g. \"deal\" → also include \"agreement\", \n"
        "    \"accord\", \"negotiations\", \"talks\", \"sanctions\")\n"
        "  \n"
        "  Examples of good keyword expansion:\n"
        "  \"iran us deal\" → [\"Iran\", \"Tehran\", \"United States\", \"Washington\",\n"
        "                    \"nuclear deal\", \"JCPOA\", \"sanctions\", \"negotiations\"]\n"
        "  \"pakistan cricket\" → [\"Pakistan\", \"PCB\", \"cricket\", \"Test match\",\n"
        "                        \"ODI\", \"T20\", \"batting\", \"bowling\"]\n"
        "  \"ukraine war\" → [\"Ukraine\", \"Russia\", \"Kyiv\", \"Moscow\", \"invasion\",\n"
        "                   \"conflict\", \"Zelensky\", \"Putin\", \"war\"]\n"
        "  \"climate change\" → [\"climate\", \"global warming\", \"emissions\", \"carbon\",\n"
        "                      \"COP\", \"fossil fuels\", \"temperature\", \"environment\"]\n\n"
        "- region: \"global\" or a specific country name if the user mentions one\n\n"
        "Rules:\n"
        f"- Today's date is {today.isoformat()}.\n"
        "- The user will provide a number of days between 1 and 14.\n"
        "  Calculate start_date by subtracting that number of days from today.\n"
        "  Set end_date to today.\n"
        "- If no day count is mentioned, default to the last 7 days.\n"
        "- If no region is mentioned, set region to \"global\".\n"
        "- Always generate 6-8 keywords minimum. Think like a journalist —\n"
        "  what words would actually appear in a headline about this topic?\n"
        "- Never use only the exact words the user typed. Always expand.\n"
        "- Never guess or invent information about the topic itself.\n"
        "- If the user's input contains spelling mistakes, silently correct \n"
        "  them before expanding keywords.\n"
        "  Example: \"iram us deel\" → treat as \"Iran US deal\"\n"
        "  Never mention the correction, just use the corrected version."
    )

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_instruction},
                  {"role": "user", "content": raw_input}],
        temperature=0,
    )
    raw_content = response.choices[0].message.content

    # Strip any markdown/code fences that may appear accidentally
    # Remove leading/trailing backticks and optional language specifier
    cleaned = re.sub(r"^```\w*\n", "", raw_content)
    cleaned = re.sub(r"\n```$", "", cleaned)
    cleaned = cleaned.strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse JSON from model response. Raw response: {raw_content}"
        ) from e

    # Success message
    print(
        f"Query parsed: {parsed.get('topic')} from {parsed.get('start_date')} to {parsed.get('end_date')}"
    )
    print(f"Keywords expanded: {parsed.get('keywords')}")
    return parsed
