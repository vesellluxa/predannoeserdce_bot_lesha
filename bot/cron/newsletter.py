import datetime
import logging

from aiogram import Bot
from utils.services import fetch_newsletters, finish_newsletter
from schemas.schemas import NewsletterSchema


async def process_newsletters(bot: Bot, username: str, password: str):
    newsletters = await fetch_newsletters(username, password)
    filtered_newsletters = [
        newsletter
        for newsletter in newsletters
        if datetime.datetime.strptime(
            newsletter.get("sending_date"), "%Y-%m-%dT%H:%M:%SZ"
        )
        <= datetime.datetime.now()
    ]
    for newsletter in filtered_newsletters:
        for user in newsletter.get("users"):
            try:
                await bot.send_message(
                    chat_id=user.get("chat_id"),
                    text=newsletter.get("text"),
                )
            except Exception as e:
                logging.error(f"Error sending newsletter: {e}")
        await finish_newsletter(newsletter.get("id"), username, password)
