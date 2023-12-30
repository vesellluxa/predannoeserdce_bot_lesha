from typing import Optional, Union

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardMarkup,
)
from constants import BOT_ANSWERS, PAGINATION
from schemas.schemas import InformationSchema


async def check_message(
    message: Message,
    text: str,
    reply_markup: Optional[
        Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]
    ] = None,
) -> None:
    """
    Check the message for a specific text and reply with the given text and optional reply markup.

    Args:
        message (Message): The message to check.
        text (str): The text to reply with.
        reply_markup (Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]], optional):
            The optional reply markup. Defaults to None.

    Returns:
        bool: True if the message has the required text attribute, False otherwise.
    """
    if not hasattr(message.text, "casefold"):
        await message.reply(
            text,
            reply_markup=reply_markup,
        )
        return False
    return True


async def delete_inline_keyboard(
    message: Message,
    bot: Bot,
) -> None:
    """
    Delete the inline keyboard and associated messages based
    on the logic of the inline keyboard rendering.

    Args:
        message (Message): The message containing the inline keyboard.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    try:
        await bot.edit_message_reply_markup(
            message.chat.id,
            message_id=message.message_id - 1,
            reply_markup=None,
        )
        await bot.delete_message(
            chat_id=message.chat.id, message_id=message.message_id - 1
        )
        await bot.delete_message(
            chat_id=message.chat.id, message_id=message.message_id - 2
        )
    except:
        try:
            await bot.edit_message_reply_markup(
                message.chat.id,
                message_id=message.message_id - 2,
                reply_markup=None,
            )
            await bot.delete_message(
                chat_id=message.chat.id, message_id=message.message_id - 1
            )
            await bot.delete_message(
                chat_id=message.chat.id, message_id=message.message_id - 2
            )
            await bot.delete_message(
                chat_id=message.chat.id, message_id=message.message_id - 3
            )
        except:
            ...


async def send_paginated_data(
    message: Message,
    shelter_information: InformationSchema,
    key: str,
    page: int,
) -> None:
    information = shelter_information.get(key)
    if not information:
        await message.answer(BOT_ANSWERS.something_went_wrong.value)
        return
    # It is better to use a list of indexes, as the indexes in the database may not be consistent if records are deleted
    indexes = list(information)
    start_idx = page * PAGINATION
    end_idx = start_idx + PAGINATION
    is_last_page = len(information) <= end_idx
    buttons = [
        [
            InlineKeyboardButton(
                text=information[indexes[i]].text,
                callback_data=f"{key}_{indexes[i]}",
            )
        ]
        for i in range(
            start_idx,
            end_idx if end_idx < len(information) else len(information),
        )
    ]
    if key == "faq" and is_last_page:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=BOT_ANSWERS.unique_question.value,
                    callback_data=f"{key}_unique",
                )
            ]
        )
    pagination_buttons = []

    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="◀️ Назад", callback_data=f"{key}_page_{page - 1}"
            )
        )
    if end_idx < len(information):
        pagination_buttons.append(
            InlineKeyboardButton(
                text="Вперед ▶️", callback_data=f"{key}_page_{page + 1}"
            )
        )

    split_pagination_buttons = [
        pagination_buttons[i : i + 2]
        for i in range(0, len(pagination_buttons), 2)
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons + split_pagination_buttons,
    )
    try:
        await message.edit_reply_markup(reply_markup=keyboard)
    except TelegramBadRequest:
        await message.answer(
            BOT_ANSWERS[key + "_reply"].value,
            reply_markup=keyboard,
        )
