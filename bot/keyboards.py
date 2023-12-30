from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)
from constants import BOT_ANSWERS
from schemas.schemas import InformationSchema


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

DATA_UPDATE_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BOT_ANSWERS.update.value),
            KeyboardButton(text=BOT_ANSWERS.delete.value),
            KeyboardButton(text=BOT_ANSWERS.back.value),
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
            KeyboardButton(text=BOT_ANSWERS.shelter.value),
            KeyboardButton(text=BOT_ANSWERS.monetary_aid.value),
            KeyboardButton(text=BOT_ANSWERS.animals.value),
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


def create_donation_keyboard(shelter_information: InformationSchema):
    donations = shelter_information.get("donations")
    buttons = []
    if donations:
        for donation in donations.values():
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=donation.text,
                        url=donation.answer,
                    ),
                ],
            )
    if buttons:
        return InlineKeyboardMarkup(inline_keyboard=buttons)
    return None


def create_animals_keyboard(shelter_information: InformationSchema):
    donations = shelter_information.get("list_animals")
    buttons = []
    if donations:
        for donation in donations.values():
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=donation.text,
                        url=donation.answer,
                    ),
                ],
            )
    if buttons:
        return InlineKeyboardMarkup(inline_keyboard=buttons)
    return None
