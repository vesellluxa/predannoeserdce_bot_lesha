import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from commands import set_main_menu
from cron.newsletter import process_newsletters
from cron.notification import process_notification
from dotenv import load_dotenv
from routers.main.middleware import BotMiddelware
from routers.main.router import router

load_dotenv()

DEBUG = os.getenv("DEBUG_MODE", default="ON").lower() in ("on", "yes", "true")
TOKEN = os.getenv("BOT_TOKEN") + "/test" if DEBUG else os.getenv("BOT_TOKEN")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(router)
    dp.callback_query.middleware(BotMiddelware(bot))
    dp.message.middleware(BotMiddelware(bot))
    dp.startup.register(set_main_menu)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        process_newsletters,
        trigger="interval",
        seconds=int(os.getenv("NEWSLETTER_INTERVAL", default=5)),
        args=[bot, os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD")],
    )
    scheduler.add_job(
        process_notification,
        trigger="interval",
        seconds=int(os.getenv("NEWSLETTER_INTERVAL", default=5)),
        args=[bot, os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD")],
    )
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
