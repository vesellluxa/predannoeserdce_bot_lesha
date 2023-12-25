import asyncio
import logging

import httpx
from constants import BOT_ANSWERS
from pydantic import ValidationError
from schemas import CreateUserDto, QuestionDto


class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def __repr__(self):
        return f"{self.question}: {self.answer}"


async def fetch_faq_questions():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/api/v1/faq")
            if response.status_code == 200:
                raw_questions = response.json()
                return {
                    raw_question.pop("id"): Question(**raw_question)
                    for raw_question in raw_questions
                }
        except httpx.HTTPError as e:
            logging.error(f"Error fetching FAQ: {e}")
    return {}


async def add_user_to_db(user: CreateUserDto):
    try:
        validated_user = CreateUserDto(**user)
        logging.info(f"Adding user to db: {validated_user}")
        await asyncio.sleep(1)
        return validated_user
    except ValidationError as e:
        logging.error(f"Error validating user: {e}")
        return None


async def add_unique_question(question: QuestionDto):
    try:
        validated_question = QuestionDto(**question)
        logging.info(f"Asking unique question: {validated_question}")
        await asyncio.sleep(1)
        return validated_question
    except ValidationError as e:
        logging.error(f"Error validating question: {e}")
        return None


async def get_shelter_info():
    logging.info("get_shelter_info")
    await asyncio.sleep(1)
    return BOT_ANSWERS.shelter_info.value
