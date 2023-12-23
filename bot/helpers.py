import requests
import httpx
import logging

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from constants import BOT_ANSWERS


class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def __repr__(self):
        return f"{self.question}: {self.answer}"


async def fetch_faq_questions():
    response = requests.get("http://127.0.0.1:3005/faq")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:3005/faq")
            if response.status_code == 200:
                raw_questions = response.json()
                return {
                    raw_question.pop("id"): Question(**raw_question)
                    for raw_question in raw_questions
                }
        except httpx.HTTPError as e:
            logging.error(f"Error fetching FAQ: {e}")
    return {}


async def add_user_to_db(user):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:3005/users", json=user
            )
            if response.status_code == 201:
                return response.json()
        except httpx.HTTPError as e:
            logging.error(f"Error adding user to db: {e}")
    return {}
