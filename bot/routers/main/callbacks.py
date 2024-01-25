from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from constants import BOT_ANSWERS
from keyboards import CANCEL_KEYBOARD, MAIN_INTERACTION_KEYBOARD, TURN_BACK_KEYBOARD
from schemas.schemas import InformationSchema
from states.states import InformationAboutShelter, PersonalDataForm
from utils.helpers import send_paginated_data
from utils.services import patch_user

from routers.main.main_interaction_handlers import process_questions


async def process_faq_callback(
        callback_query: CallbackQuery,
        shelter_information: InformationSchema,
        bot: Bot,
        state: FSMContext,
) -> None:
    data, question_id = callback_query.data.split("_")
    global LAST_CATEGORY
    LAST_CATEGORY = data
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
            text=question.answer,
            chat_id=callback_query.message.chat.id,
            message_id=message,
            reply_markup=TURN_BACK_KEYBOARD
        )
    except Exception as e:

        print(e)
        await callback_query.message.answer(question.answer)


async def process_page_callback(
        callback_query: CallbackQuery, shelter_information: InformationSchema
) -> None:
    key, _, page = callback_query.data.split("_")
    await send_paginated_data(
        callback_query.message, shelter_information, key, int(page)
    )


async def process_personal_data_consent(
        callback_query: CallbackQuery, state: FSMContext, access: str = None
) -> None:
    print(access)
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
        "faq": BOT_ANSWERS.faq_reply,
        "info": BOT_ANSWERS.info_reply,
        "needs": BOT_ANSWERS.needs_reply
    }
    return values[category]


async def process_back_to_questions_callback(
        callback_query: CallbackQuery,
        bot: Bot,
        state: FSMContext,
        shelter_information: InformationSchema
) -> None:
    await callback_query.answer()  # Ответить на callback query

    # Возможно, вам нужно установить соответствующее состояние перед отображением вопросов
    await state.set_state(InformationAboutShelter.questions)

    await bot.edit_message_text(
        text=get_message_text(LAST_CATEGORY),
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=TURN_BACK_KEYBOARD
    )

    # Вызываем process_questions, предоставляя ему необходимые параметры
    # Так как process_questions ожидает объект Message, мы используем callback_query.message
    await process_questions(
        message=callback_query.message,
        bot=bot,
        shelter_information=shelter_information,
        category=LAST_CATEGORY
    )
