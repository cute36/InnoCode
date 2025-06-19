from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))  # Список ID администраторов
# Настройки прокси
PROXY_ENABLED = True  # Можно отключать прокси при необходимости
PROXY_MAX_RETRIES = 2