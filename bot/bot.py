import asyncio
import django
import logging
import os
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faithful_heart.settings')
django.setup()


load_dotenv(dotenv_path="./bot/.env")

DEBUG = os.getenv("DEBUG_MODE", default="ON").lower() in ("on", "yes", "true")

TOKEN = os.getenv("BOT_TOKEN") + "/test" if DEBUG else ""
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    logging.info(message.text)
    await message.answer("Тут будет инструкция по использованию бота")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    logging.info(message.text)
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Тип данных для копирования не поддерживается")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


async def send_request(url, data, user_id):
    ping_response = requests.get('http://127.0.0.1:8000/api/ping/')
    if ping_response.status_code == 200:
        queryset = OutstandingToken.objects.filter(user_id=user_id)
        token = queryset.first().token
        if token:
            headers = {'Authorization': f'Bearer {token}'}
            return requests.post(url, data=data, headers=headers)
        else:
            return 'Токен не найден'
    else:
        return 'Сервер не доступен'


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
