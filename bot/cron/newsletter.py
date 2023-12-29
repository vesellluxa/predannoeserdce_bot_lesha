import datetime
import logging

from aiogram import Bot
from utils.services import fetch_newsletters


async def process_newsletters(bot: Bot, username: str, password: str):
    newsletters = await fetch_newsletters(username, password)
    if not newsletters.get("users"):
        return
    users = newsletters["users"]
    if not newsletters.get("newsletters"):
        return
    newsletters = newsletters["newsletters"]
    filtered_newsletters = [
        newsletter
        for newsletter in newsletters
        if not newsletter.get("finished")
        and newsletter.get("date") <= datetime.datetime.now()
    ]
    for newsletter in filtered_newsletters:
        for user in users:
            try:
                await bot.send_message(
                    chat_id=user.get("chat_id"),
                    text=newsletter.get("text"),
                )
            except Exception as e:
                logging.error(f"Error sending newsletter: {e}")
        newsletter["finished"] = True
