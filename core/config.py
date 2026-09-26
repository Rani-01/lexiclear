import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-2.5-flash"

DISCLAIMER_TEXT = (
    "LexiClear provides AI-powered informational summaries and document analysis. "
    "It does not constitute formal legal advice or create an attorney-client relationship."
)