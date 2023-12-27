import logging


from aiogram import F, Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from constants import BOT_ANSWERS, PAGINATION, NEEDS
from helpers import (
    add_unique_question,
    add_user_to_db,
    patch_user,
    check_user_status,
)
from keyboards import (
    CANCEL_KEYBOARD,
    FAQ_INFO_CANCEL_KEYBOARD,
    TRY_AGAIN_KEYBOARD,
    YES_NO_KEYBOARD,
    send_main_interaction_buttons,
)
from middleware import FetchingMiddleware, TokenMiddleware
from schemas import InformationSchema

router = Router()
router.message.middleware(TokenMiddleware())
router.message.middleware(FetchingMiddleware())
router.callback_query.middleware(FetchingMiddleware())


class PersonalDataForm(StatesGroup):
    permission = State()
    first_name = State()
    second_name = State()
    surname = State()
    email = State()
    phone = State()


class InformationAboutShelter(StatesGroup):
    main_interaction = State()
    questions = State()
    unique_question = State()


@router.message(CommandStart())
async def command_start(
    message: Message, state: FSMContext, access: str = None
) -> None:
    if not access:
        await state.set_state(InformationAboutShelter.main_interaction)
        await message.answer(BOT_ANSWERS.something_went_wrong.value)
        return
    await state.set_state(PersonalDataForm.permission)
    user = {
        "chat_id": message.chat.id,
        "username": message.chat.username,
    }
    user_db = await add_user_to_db(user, access)
    if user_db is None:
        await message.answer(
            BOT_ANSWERS.user_creation_error.value,
            reply_markup=YES_NO_KEYBOARD,
        )
        return
    if user_db.get("details") == "User already exists":
        user_status = await check_user_status(message.chat.id, access)
        if user_status.get("is_fully_filled"):
            await state.set_state(InformationAboutShelter.main_interaction)
            await send_main_interaction_buttons(
                message, BOT_ANSWERS.greeting_full_data.value
            )
        else:
            await state.set_state(PersonalDataForm.permission)
            await message.answer(
                BOT_ANSWERS.greeting_partial_data.value,
                reply_markup=YES_NO_KEYBOARD,
            )
    else:
        await message.answer(
            BOT_ANSWERS.greeting.value, reply_markup=YES_NO_KEYBOARD
        )


@router.message(
    PersonalDataForm.first_name,
    F.text.casefold() == BOT_ANSWERS.cancel.value.casefold(),
)
@router.message(
    PersonalDataForm.surname,
    F.text.casefold() == BOT_ANSWERS.cancel.value.casefold(),
)
@router.message(
    PersonalDataForm.email,
    F.text.casefold() == BOT_ANSWERS.cancel.value.casefold(),
)
@router.message(
    PersonalDataForm.phone,
    F.text.casefold() == BOT_ANSWERS.cancel.value.casefold(),
)
@router.message(
    InformationAboutShelter.main_interaction,
    F.text.casefold() == BOT_ANSWERS.cancel.value.casefold(),
)
@router.message(
    InformationAboutShelter.questions,
    F.text.casefold() == BOT_ANSWERS.cancel.value.casefold(),
)
@router.message(
    InformationAboutShelter.unique_question,
    F.text.casefold() == BOT_ANSWERS.cancel.value.casefold(),
)
async def process_cancel(message: Message, state: FSMContext) -> None:
    await state.set_state(InformationAboutShelter.main_interaction)
    await send_main_interaction_buttons(
        message, BOT_ANSWERS.greeting_full_data.value
    )


@router.message(
    PersonalDataForm.permission,
    (F.text.casefold() == BOT_ANSWERS.no.value.casefold())
    | (F.text.casefold() == BOT_ANSWERS.yes.value.casefold())
    | (F.text.casefold() == BOT_ANSWERS.try_again.value.casefold()),
)
async def process_permission(message: Message, state: FSMContext) -> None:
    if message.text.casefold() == BOT_ANSWERS.no.value.casefold():
        await state.set_state(InformationAboutShelter.main_interaction)
        await send_main_interaction_buttons(
            message, BOT_ANSWERS.permission.value
        )
    else:
        await state.set_state(PersonalDataForm.first_name)
        await message.answer(
            BOT_ANSWERS.name.value,
            reply_markup=CANCEL_KEYBOARD,
        )


@router.message(PersonalDataForm.first_name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(PersonalDataForm.surname)
    await message.answer(BOT_ANSWERS.surname.value)


@router.message(PersonalDataForm.surname)
async def process_surname(message: Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    await state.set_state(PersonalDataForm.email)
    await message.answer(
        BOT_ANSWERS.email.value,
    )


@router.message(PersonalDataForm.email)
async def process_email(message: Message, state: FSMContext) -> None:
    await state.update_data(email=message.text)
    await state.set_state(PersonalDataForm.phone)
    await message.answer(BOT_ANSWERS.phone.value)

    # await message.answer(
    #     f"Ваш номер: {message.contact.phone_number}, верно?",
    #     reply_markup=YES_NO_KEYBOARD,
    # )


@router.message(
    PersonalDataForm.phone,
)
async def process_phone(
    message: Message, state: FSMContext, access: str = ""
) -> None:
    """if message.text.casefold() == BOT_ANSWERS.no.value.casefold():
        await message.answer(BOT_ANSWERS.phone.value)
        return
    elif message.text.casefold() == BOT_ANSWERS.yes.value.casefold():
        data = await state.update_data(phone=message.contact.phone_number)
    else:
        data = await state.update_data(phone=message.text)"""
    if access == "":
        await state.set_state(InformationAboutShelter.main_interaction)
        await message.answer(BOT_ANSWERS.something_went_wrong.value)
        return
    data = await state.update_data(phone=message.text)
    user = {
        "name": data["first_name"],
        "surname": data["surname"],
        "email": data["email"],
        "phone": data["phone"],
        "chat_id": message.chat.id,
        "username": message.chat.username,
    }
    user_db = await patch_user(user, access)
    if user_db is None:
        await state.set_state(PersonalDataForm.permission)
        await message.answer(
            BOT_ANSWERS.validation_error.value, reply_markup=TRY_AGAIN_KEYBOARD
        )
        return
    await state.clear()
    await state.set_state(InformationAboutShelter.main_interaction)
    await send_main_interaction_buttons(
        message, BOT_ANSWERS.registration_message.value
    )


@router.message(
    InformationAboutShelter.main_interaction,
    (
        (F.text.casefold() == BOT_ANSWERS.unique_question.value.casefold())
        | (F.text.casefold() == BOT_ANSWERS.shelter.value.casefold())
    ),
)
async def process_main_interaction(
    message: Message, state: FSMContext
) -> None:
    if message.text.casefold() == BOT_ANSWERS.unique_question.value.casefold():
        await state.set_state(InformationAboutShelter.unique_question)
        await message.answer(BOT_ANSWERS.enter_unique_question.value)
    elif message.text.casefold() == BOT_ANSWERS.shelter.value.casefold():
        await state.set_state(InformationAboutShelter.questions)
        await message.answer(
            BOT_ANSWERS.questions_title.value,
            reply_markup=FAQ_INFO_CANCEL_KEYBOARD,
        )


@router.message(
    InformationAboutShelter.questions,
    (
        (F.text.casefold() == BOT_ANSWERS.faq.value.casefold())
        | (F.text.casefold() == BOT_ANSWERS.shelter.value.casefold())
        | (F.text.casefold() == BOT_ANSWERS.needs.value.casefold())
    ),
)
async def process_questions(
    message: Message,
    shelter_information: InformationSchema = {},
) -> None:
    if message.text.casefold() == BOT_ANSWERS.faq.value.casefold():
        await send_paginated_data(message, shelter_information, "faq", 0)
    elif message.text.casefold() == BOT_ANSWERS.shelter.value.casefold():
        await send_paginated_data(message, shelter_information, "info", 0)
    elif message.text.casefold() == BOT_ANSWERS.needs.value.casefold():
        buttons = [
            [
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"needs_{text}",
                )
            ]
            for text in ["Срочные нужды", "Аптека обычная"]
        ]
        await message.answer(
            BOT_ANSWERS.needs_info.value,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        )


@router.message(InformationAboutShelter.unique_question)
async def process_unique_question(
    message: Message, state: FSMContext, access: str = ""
) -> None:
    if access == "":
        await state.set_state(InformationAboutShelter.main_interaction)
        await message.answer(BOT_ANSWERS.something_went_wrong.value)
        return
    question = {"text": message.text, "owner": message.chat.id}
    question_db = await add_unique_question(question, access)
    if question_db is None:
        await state.set_state(InformationAboutShelter.main_interaction)
        await message.answer(BOT_ANSWERS.question_creation_error.value)
        return
    await state.set_state(InformationAboutShelter.main_interaction)
    await message.answer(BOT_ANSWERS.unique_question_reply.value)


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
    if page > 0:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="◀️ Назад", callback_data=f"{key}_page_{page - 1}"
                )
            ]
        )
    if end_idx < len(information):
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Вперед ▶️", callback_data=f"{key}_page_{page + 1}"
                )
            ]
        )

    try:
        await message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=buttons,
            )
        )
    except TelegramBadRequest:
        await message.answer(
            BOT_ANSWERS.faq.value,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        )


@router.callback_query(
    (F.data.contains("faq_") | F.data.contains("info_"))
    & ~F.data.contains("page_")
)
async def process_faq_callback(
    callback_query: CallbackQuery, shelter_information: InformationSchema
) -> None:
    data, quiestion_id = callback_query.data.split("_")
    question = shelter_information.get(data).get(int(quiestion_id))
    if question is None:
        await callback_query.answer("Информация не найдена")
        return
    await callback_query.message.answer(question.answer)


@router.callback_query(F.data.contains("page_"))
async def process_page_callback(
    callback_query: CallbackQuery, shelter_information: InformationSchema
) -> None:
    key, _, page = callback_query.data.split("_")
    await send_paginated_data(
        callback_query.message, shelter_information, key, int(page)
    )


@router.callback_query(F.data.contains("needs_"))
async def process_page_callback(
    callback_query: CallbackQuery, bot: Bot
) -> None:
    key = callback_query.data.split("_")[1]
    message = callback_query.message.message_id
    try:
        await bot.edit_message_text(
            text=NEEDS[key],
            chat_id=callback_query.message.chat.id,
            message_id=message + 1,
        )
    except Exception as e:
        await callback_query.message.answer(NEEDS[key])
