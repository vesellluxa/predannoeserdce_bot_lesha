import logging
import urllib.parse

import httpx
from pydantic import ValidationError
from schemas import CreateQuestionDto, CreateUserShortDto, UpdateUser


async def fetch_data(endpoint: str, access: str):
    data = []
    async with httpx.AsyncClient() as client:
        try:
            next_page = f"http://127.0.0.1:8000/api/v1/{endpoint}"
            while next_page:
                response = await client.get(
                    urllib.parse.unquote(next_page),
                    headers={"Authorization": f"Bearer {access}"},
                )
                if response.status_code == 200:
                    data.extend(response.json().get("results"))
                    next_page = response.json().get("next")

        except httpx.HTTPError as e:
            logging.error(f"Error fetching data from endpoint {endpoint}: {e}")
    return data


async def obtain_token(username: str, password: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://127.0.0.1:8000/api/v1/obtain_token/",
                data={"username": username, "password": password},
            )
            if response.status_code == 200:
                return response.json()
        except httpx.HTTPError as e:
            logging.error(f"Error fetching Token: {e}")
    return {}


async def refresh_token(refresh_token: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://127.0.0.1:8000/api/token/refresh/",
                data={"refresh": refresh_token},
            )
            if response.status_code == 200:
                return response.json()
        except httpx.HTTPError as e:
            logging.error(f"Error refreshing Token: {e}")
    return {}


async def add_user_to_db(user: CreateUserShortDto, access: str):
    async with httpx.AsyncClient() as client:
        try:
            validated_user = CreateUserShortDto(**user)
            response = await client.post(
                "http://127.0.0.1:8000/api/v1/users/",
                json=validated_user.model_dump(),
                headers={"Authorization": f"Bearer {access}"},
            )
            if response.status_code == 201:
                return response.json()
            if response.status_code == 400:
                response = response.json()
                if response.get("username") == [
                    "telegram user с таким Имя пользователя уже существует."
                ]:
                    return {"details": "User already exists"}
        except httpx.HTTPError as e:
            logging.error(f"Error adding user to DB: {e}")
        except ValidationError as e:
            logging.error(f"Error validating user: {e}")
    return None


async def check_user_status(chat_id: int, access: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"http://127.0.0.1:8000/api/v1/users/{chat_id}/get_state/",
                headers={"Authorization": f"Bearer {access}"},
            )
            if response.status_code == 200:
                return response.json()
        except httpx.HTTPError as e:
            logging.error(f"Error adding user to DB: {e}")
        except ValidationError as e:
            logging.error(f"Error validating user: {e}")
    return None


async def patch_user(user: UpdateUser, access: str):
    async with httpx.AsyncClient() as client:
        try:
            validated_user = UpdateUser(**user)
            response = await client.patch(
                f"http://127.0.0.1:8000/api/v1/users/{validated_user.chat_id}/",
                json=validated_user.model_dump(),
                headers={"Authorization": f"Bearer {access}"},
            )
            if response.status_code == 200:
                return response.json()
        except httpx.HTTPError as e:
            logging.error(f"Error updating user data: {e}")
        except ValidationError as e:
            logging.error(f"Error validating user data: {e}")
    return None


async def add_unique_question(question: CreateQuestionDto, access: str):
    async with httpx.AsyncClient() as client:
        try:
            validated_question = CreateQuestionDto(**question)
            response = await client.post(
                "http://127.0.0.1:8000/api/v1/unique_question/",
                json=validated_question.model_dump(),
                headers={"Authorization": f"Bearer {access}"},
            )
            if response.status_code == 201:
                return response.json()
        except httpx.HTTPError as e:
            logging.error(f"Error adding unique question to DB: {e}")
        except ValidationError as e:
            logging.error(f"Error validating question: {e}")
    return None
