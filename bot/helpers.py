from typing import Optional, Union

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, Message, ReplyKeyboardMarkup


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
