import os
from dotenv import load_dotenv

# Загрузка переменных среды из файла .env
load_dotenv()

TOKEN = os.getenv("TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")