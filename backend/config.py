import os
from dotenv import load_dotenv

load_dotenv()
app_env = os.getenv("app_env", "Development")
if app_env != "Development":
    GROQ_API_KEY = ""
else:
    GROQ_API_KEY = "" #develop

CONFIG = {
    "GROQ_API_KEY": GROQ_API_KEY,
    "ENV": app_env
}