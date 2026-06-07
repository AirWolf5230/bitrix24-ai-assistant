import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://172.17.32.1:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma4:latest")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")