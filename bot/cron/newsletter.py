import datetime
import logging

from aiogram import Bot
from utils.services import (
    fetch_notifications_and_newsletters,
    finish_notification_or_newsletter,
)


async def process_newsletters(bot: Bot, username: str, password: str):
    newsletters = await fetch_notifications_and_newsletters(username, password)
    if not newsletters:
        return None
    filtered_newsletters = [
        newsletter
        for newsletter in newsletters
        if datetime.datetime.fromisoformat(newsletter.get("sending_date"))
        <= datetime.datetime.now(
            tz=datetime.timezone(datetime.timedelta(hours=3))
        )
    ]
    for newsletter in filtered_newsletters:
        for chat_id in newsletter.get("users"):
            try:
                await bot.send_message(
                    chat_id=chat_id,
                    text=newsletter.get("text"),
                )
            except Exception as e:
                logging.error(f"Error sending newsletter: {e}")
        await finish_notification_or_newsletter(
            newsletter.get("id"), username, password
        )
