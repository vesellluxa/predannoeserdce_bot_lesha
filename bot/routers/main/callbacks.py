import datetime
import logging

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from constants import BOT_ANSWERS
from keyboards import (
    CANCEL_KEYBOARD,
    MAIN_INTERACTION_KEYBOARD,
    TURN_BACK_KEYBOARD,
)
from routers.main.main_interaction_handlers import process_questions
from schemas.schemas import InformationSchema
from states.states import InformationAboutShelter, PersonalDataForm
from utils.helpers import send_paginated_data
from utils.services import patch_user


async def process_faq_callback(
    callback_query: CallbackQuery,
    shelter_information: InformationSchema,
    bot: Bot,
    helper: dict,
    state: FSMContext,
) -> None:
    data, question_id = callback_query.data.split("_")

    info = helper.get(callback_query.message.chat.id)
    if info is None:
        helper[callback_query.message.chat.id] = {
            "last_category": data,
            "time": datetime.datetime.now(),
        }
    else:
        info.update({"last_category": data, "time": datetime.datetime.now()})

    print(helper)
    if question_id == "unique":
        await state.set_state(InformationAboutShelter.unique_question)
        await callback_query.message.answer(
            BOT_ANSWERS.enter_unique_question.value,
            reply_markup=CANCEL_KEYBOARD,
        )
        return
    question = shelter_information.get(data).get(int(question_id))
    if question is None:
        await callback_query.answer("Информация не найдена")
        return
    message = callback_query.message.message_id

    try:
        await bot.edit_message_text(
            text=f"Вопрос: {question.text}\n" f"Ответ: {question.answer}",
            chat_id=callback_query.message.chat.id,
            message_id=message,
            reply_markup=TURN_BACK_KEYBOARD,
        )
    except Exception as e:
        logging.error(e)
        await callback_query.message.answer(question.answer)


async def process_page_callback(
    callback_query: CallbackQuery,
    shelter_information: InformationSchema,
    helper: dict,
) -> None:
    key, _, page = callback_query.data.split("_")

    info = helper.get(callback_query.message.chat.id)
    if info is None:
        helper[callback_query.message.chat.id] = {
            "last_page": int(page),
            "time": datetime.datetime.now(),
        }
    else:
        info.update({"last_page": int(page), "time": datetime.datetime.now()})

    await send_paginated_data(
        callback_query.message, shelter_information, key, int(page)
    )


async def process_personal_data_consent(
    callback_query: CallbackQuery, state: FSMContext, access: str = None
) -> None:
    _, _, _, consent = callback_query.data.split("_")
    if consent == "agree":
        await state.set_state(PersonalDataForm.name)
        await callback_query.message.answer(
            BOT_ANSWERS.name.value, reply_markup=CANCEL_KEYBOARD
        )
    else:
        await state.set_state(InformationAboutShelter.main_interaction)
        user = {
            "name": "",
            "middle_name": "",
            "surname": "",
            "phone_number": None,
            "email": None,
            "chat_id": callback_query.message.chat.id,
            "username": callback_query.message.chat.username.lower(),
            "consent_to_save_personal_data": False,
        }
        await patch_user(user, access)
        await callback_query.message.answer(
            BOT_ANSWERS.permission.value,
            reply_markup=MAIN_INTERACTION_KEYBOARD,
        )


def get_message_text(category):
    values = {
        "faq": BOT_ANSWERS.faq_reply.value,
        "info": BOT_ANSWERS.info_reply.value,
        "needs": BOT_ANSWERS.needs_reply.value,
    }
    return values[category]


async def process_back_to_questions_callback(
    callback_query: CallbackQuery,
    bot: Bot,
    shelter_information: InformationSchema,
    helper: dict,
) -> None:
    await callback_query.answer()

    info = helper.get(callback_query.message.chat.id)
    if info is None:
        category = "faq"
        page = 0
    else:
        category = info.get("last_category", "faq")
        page = info.get("last_page", 0)

    await bot.edit_message_text(
        text=get_message_text(category),
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=TURN_BACK_KEYBOARD,
    )

    await process_questions(
        message=callback_query.message,
        bot=bot,
        shelter_information=shelter_information,
        category=category,
        page=page,
    )
