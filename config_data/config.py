import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

TELEGRAM_BOT_KEY = os.getenv("TELEGRAM_BOT_KEY")
API_KEY = os.getenv("API_KEY")

