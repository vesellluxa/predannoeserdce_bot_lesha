import datetime
import os
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message
from dotenv import load_dotenv
from schemas import Question
from services import fetch_data, obtain_token, refresh_token

load_dotenv(dotenv_path="./bot/.env")


class BotMiddelware(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        data["bot"] = self.bot
        return await handler(event, data)


class TokenMiddleware(BaseMiddleware):
    _access_token = None
    _refresh_token = None
    _instance = None
    _last_token_refresh_time = None
    TOKEN_LIFETIME = datetime.timedelta(minutes=5)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenMiddleware, cls).__new__(cls)
        return cls._instance

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not self._access_token:
            response = await obtain_token(
                os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD")
            )
            if not response:
                return await handler(event, data)
            self._access_token = response.get("access")
            self._refresh_token = response.get("refresh")
            self._last_token_refresh_time = datetime.datetime.now()
        if (
            self._access_token
            and self._refresh_token
            and self._token_refresh_required()
        ):
            response = await refresh_token(self._refresh_token)
            if not response:
                response = await obtain_token(
                    os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD")
                )
                if not response:
                    return await handler(event, data)
                self._access_token = response.get("access")
                self._refresh_token = response.get("refresh")
                self._last_token_refresh_time = datetime.datetime.now()
            self._last_token_refresh_time = datetime.datetime.now()
            self._access_token = response.get("access")
        data["access"] = self._access_token
        return await handler(event, data)

    def _token_refresh_required(self) -> bool:
        return (
            self._last_token_refresh_time is None
            or datetime.datetime.now() - self._last_token_refresh_time
            > self.TOKEN_LIFETIME
        )


class FetchingMiddleware(BaseMiddleware):
    _instance = None
    _shelter_information = {
        "faq": {},
        "info": {},
        "needs": {},
    }
    _last_fetch_time = {
        "faq": None,
        "info": None,
        "needs": None,
    }
    _endpoints = {
        "faq": "faq/?category=Shelter_Info",
        "info": "faq/?category=FAQ",
        "needs": "faq/?category=Needs",
    }
    FETCH_INTERVAL = datetime.timedelta(minutes=10)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FetchingMiddleware, cls).__new__(cls)
        return cls._instance

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        for key, endpoint in self._endpoints.items():
            if not self._shelter_information[key] or self._fetch_required(key):
                response = await fetch_data(endpoint, data.get("access"))
                if not response:
                    return await handler(event, data)
                self._shelter_information[key] = {
                    raw_question.pop("id"): Question(**raw_question)
                    for raw_question in response
                }
                self._last_fetch_time[key] = datetime.datetime.now()

        data["shelter_information"] = self._shelter_information
        return await handler(event, data)

    def _fetch_required(self, endpoint: str) -> bool:
        return (
            self._last_fetch_time[endpoint] is None
            or datetime.datetime.now() - self._last_fetch_time[endpoint]
            > self.FETCH_INTERVAL
        )
