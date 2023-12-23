import datetime
from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from helpers import fetch_faq_questions


class QuestionsMiddelware(BaseMiddleware):
    """
    Middleware class for handling FAQ questions.

    This middleware fetches FAQ questions and stores them in the `questions` attribute of the data dictionary.
    It ensures that the questions are fetched only once every 10 minutes to reduce unnecessary API calls.

    Attributes:
        _instance (QuestionsMiddelware): Singleton instance of the class.
        _questions (dict[int, Questions]]): dictionary of FAQ questions.
        _last_fetch_time (datetime.datetime): Timestamp of the last fetch operation.
    """

    _instance = None
    _questions = None
    _last_fetch_time = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QuestionsMiddelware, cls).__new__(cls)
        return cls._instance

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not self._questions:
            self._questions = await fetch_faq_questions()
            self._last_fetch_time = datetime.datetime.now()
        if (
            datetime.datetime.now() - self._last_fetch_time
            > datetime.timedelta(minutes=10)
        ):
            self._questions = await fetch_faq_questions()
            self._last_fetch_time = datetime.datetime.now()
        data["questions"] = self._questions
        return await handler(event, data)
