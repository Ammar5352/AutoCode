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