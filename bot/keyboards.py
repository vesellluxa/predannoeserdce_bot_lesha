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
    input_field_placeholder="Выберите вариант: ",
)

SEND_CONTACT_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text=BOT_ANSWERS.send_contact.value, request_contact=True
            ),
            KeyboardButton(text=BOT_ANSWERS.cancel.value),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Введите номер телефона: ",
)

CANCEL_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BOT_ANSWERS.cancel.value),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Сообщение: ",
)

TRY_AGAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BOT_ANSWERS.try_again.value),
            KeyboardButton(text=BOT_ANSWERS.cancel.value),
        ]
    ],
    resize_keyboard=True,
)

FAQ_INFO_CANCEL_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BOT_ANSWERS.faq.value),
            KeyboardButton(text=BOT_ANSWERS.info.value),
        ],
        [
            KeyboardButton(text=BOT_ANSWERS.needs.value),
            KeyboardButton(text=BOT_ANSWERS.cancel.value),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите категорию: ",
)

MAIN_INTERACTION_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BOT_ANSWERS.unique_question.value),
            KeyboardButton(text=BOT_ANSWERS.shelter.value),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите категорию: ",
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
    await message.answer(text, reply_markup=MAIN_INTERACTION_KEYBOARD)
