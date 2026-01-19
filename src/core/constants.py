# core/logger.py
LOG_FORMAT = "%Y-%m-%d %H:%M:%S"
FILE_ENCODER = "utf-8"

# infrastructure/groq.py
AI_TEMPERATURE = 0.1
ANSWER_FORMAT = {"type": "json_object"}

# infrastructure/google_sheets.py
GOOGLE_SHEETS_URLS = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]