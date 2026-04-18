import os
from dotenv import load_dotenv

load_dotenv()
app_env = os.getenv("app_env", "Development")
if app_env != "Development":
    GROQ_API_KEY = "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"
else:
    GROQ_API_KEY = "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" #develop

CONFIG = {
    "GROQ_API_KEY": GROQ_API_KEY,
    "ENV": app_env
}