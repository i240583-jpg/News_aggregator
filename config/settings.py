import os
from dotenv import load_dotenv

load_dotenv()

required_keys = ["OPENAI_API_KEY", "NEWSAPI_KEY", "GNEWS_KEY"]
missing = [key for key in required_keys if not os.getenv(key)]

if missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

print("Config loaded successfully.")
