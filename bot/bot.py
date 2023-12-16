import asyncio
import logging
import os
import sys

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
dp = Dispatcher()


class Registration(StatesGroup):
    username = State()
    email = State()
    password = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message(StateFilter(None), Command('register'))
async def start_registration(message: Message, state: FSMContext):
    await message.answer(text="Введите username")
    await state.set_state(Registration.username)


@dp.message(Registration.username)
async def process_registration_email(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Введите email")
    await state.set_state(Registration.email)


@dp.message(Registration.email)
async def process_registration_pass(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите пароль")
    await state.set_state(Registration.password)


@dp.message(Registration.password)
async def end_registration(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    url = 'http://127.0.0.1:8000/api/users/'
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            await message.answer('Регистрация прошла успешно')
        else:
            await message.answer(f'Ошибка при регистрации: {response.content}')
    except requests.exceptions.RequestException as e:
        await message.answer(f'Ошибка при отправке запроса: {e}')
    await state.clear()


class Login(StatesGroup):
    username = State()
    password = State()


@dp.message(StateFilter(None), Command('login'))
async def start_login(message: Message, state: FSMContext):
    await message.answer(text="Введите username")
    await state.set_state(Login.username)


@dp.message(Login.username)
async def process_login(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Введите пароль")
    await state.set_state(Login.password)


@dp.message(Login.password)
async def end_login(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    url = 'http://127.0.0.1:8000/api/auth/token/login/'
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            await message.answer('Аутентификация прошла успешно')
            # token = response.json().get('auth_token', '')
        else:
            await message.answer(
                f'Ошибка при aутентификация: {response.content}'
            )
    except requests.exceptions.RequestException as e:
        await message.answer(f'Ошибка при отправке запроса: {e}')
    await state.clear()


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    logging.info(message.text)
    await message.answer('Тут будет инструкция по использованию бота')


@dp.message()
async def echo_handler(message: types.Message) -> None:
    logging.info(message.text)
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer('Тип данных для копирования не поддерживается')


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
