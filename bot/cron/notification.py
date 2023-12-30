import logging

from aiogram import Bot
from utils.services import (
    fetch_notifications_and_newsletters,
    finish_notification_or_newsletter,
)


async def process_notification(bot: Bot, username: str, password: str):
    notifications = await fetch_notifications_and_newsletters(
        username, password, type="notifications"
    )
    if not notifications:
        return None

    for notification in notifications:
        try:
            await bot.send_message(
                chat_id=notification.get("to").get("chat_id"),
                text=notification.get("text"),
            )
        except Exception as e:
            logging.error(f"Error sending newsletter: {e}")
        await finish_notification_or_newsletter(
            notification.get("id"), username, password, type="notifications"
        )
