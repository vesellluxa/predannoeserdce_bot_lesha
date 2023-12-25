from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from constants import BOT_ANSWERS

YES_NO_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BOT_ANSWERS.yes.value),
            KeyboardButton(text=BOT_ANSWERS.no.value),
        ]
    ],
    resize_keyboard=True,
)

CANCEL_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BOT_ANSWERS.cancel.value),
        ]
    ],
    resize_keyboard=True,
)

TRY_AGAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BOT_ANSWERS.try_again.value),
        ]
    ],
    resize_keyboard=True,
)


FAQ_UNIQUE_CANCEL_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BOT_ANSWERS.faq.value),
            KeyboardButton(text=BOT_ANSWERS.unique_question.value),
            KeyboardButton(text=BOT_ANSWERS.shelter.value),
            KeyboardButton(text=BOT_ANSWERS.cancel.value),
        ]
    ],
    resize_keyboard=True,
)


async def send_main_interaction_buttons(message: Message, text: str) -> None:
    """
    Sends a message with main interaction buttons.

    Args:
      message (Message): The message object to reply to.
      text (str): The text of the message.

    Returns:
      None
    """
    keyboard = [
        [
            KeyboardButton(text=BOT_ANSWERS.questions.value),
            KeyboardButton(text=BOT_ANSWERS.shelter.value),
        ]
    ]
    await message.answer(
        text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
        ),
    )
