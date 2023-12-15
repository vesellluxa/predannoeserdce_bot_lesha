import os

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

api_id = os.getenv("APP_ID")
api_hash = os.getenv("APP_HASH")


with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("Session string:", client.session.save())
