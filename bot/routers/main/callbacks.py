from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from constants import BOT_ANSWERS
from keyboards import CANCEL_KEYBOARD, MAIN_INTERACTION_KEYBOARD
from schemas.schemas import InformationSchema
from states.states import InformationAboutShelter, PersonalDataForm
from utils.helpers import send_paginated_data


async def process_faq_callback(
    callback_query: CallbackQuery,
    shelter_information: InformationSchema,
    bot: Bot,
    state: FSMContext,
) -> None:
    data, quiestion_id = callback_query.data.split("_")
    if quiestion_id == "unique":
        await state.set_state(InformationAboutShelter.unique_question)
        await callback_query.message.answer(
            BOT_ANSWERS.enter_unique_question.value,
            reply_markup=CANCEL_KEYBOARD,
        )
        return
    question = shelter_information.get(data).get(int(quiestion_id))
    if question is None:
        await callback_query.answer("Информация не найдена")
        return
    message = callback_query.message.message_id
    try:
        await bot.edit_message_text(
            text=question.answer,
            chat_id=callback_query.message.chat.id,
            message_id=message + 1,
        )
    except Exception as e:
        await callback_query.message.answer(question.answer)


async def process_page_callback(
    callback_query: CallbackQuery, shelter_information: InformationSchema
) -> None:
    key, _, page = callback_query.data.split("_")
    await send_paginated_data(
        callback_query.message, shelter_information, key, int(page)
    )


async def process_personal_data_consent(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    _, _, _, consent = callback_query.data.split("_")
    if consent == "agree":
        await state.set_state(PersonalDataForm.name)
        await callback_query.message.answer(
            BOT_ANSWERS.name.value, reply_markup=CANCEL_KEYBOARD
        )
    else:
        await state.set_state(InformationAboutShelter.main_interaction)
        await callback_query.message.answer(
            BOT_ANSWERS.permission.value,
            reply_markup=MAIN_INTERACTION_KEYBOARD,
        )
