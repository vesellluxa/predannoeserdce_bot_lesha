import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from middleware import BotMiddelware
from router import router

load_dotenv()

DEBUG = os.getenv("DEBUG_MODE", default="ON").lower() in ("on", "yes", "true")
TOKEN = os.getenv("BOT_TOKEN") + "/test" if DEBUG else os.getenv("BOT_TOKEN")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    dp.callback_query.middleware(BotMiddelware(bot))
    dp.message.middleware(BotMiddelware(bot))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
