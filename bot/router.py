from aiogram import Bot, F, Router
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
from constants import BOT_ANSWERS, PAGINATION
from helpers import check_message, delete_inline_keyboard
from keyboards import (
    CANCEL_KEYBOARD,
    FAQ_INFO_CANCEL_KEYBOARD,
    MAIN_INTERACTION_KEYBOARD,
    SEND_CONTACT_KEYBOARD,
    TRY_AGAIN_KEYBOARD,
    YES_NO_KEYBOARD,
    send_main_interaction_buttons,
)
from middleware import FetchingMiddleware, TokenMiddleware
from schemas import InformationSchema
from services import (
    add_unique_question,
    add_user_to_db,
    check_user_status,
    patch_user,
)

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
    phone_number = State()


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
    PersonalDataForm.phone_number,
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
async def process_cancel(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    await state.set_state(InformationAboutShelter.main_interaction)
    await delete_inline_keyboard(message, bot)
    await send_main_interaction_buttons(
        message, BOT_ANSWERS.greeting_full_data.value
    )


@router.message(PersonalDataForm.permission)
async def process_permission(message: Message, state: FSMContext) -> None:
    responses = {
        BOT_ANSWERS.no.value.casefold(): {
            "state": InformationAboutShelter.main_interaction,
            "message": BOT_ANSWERS.permission.value,
            "keyboard": MAIN_INTERACTION_KEYBOARD,
        },
        BOT_ANSWERS.yes.value.casefold(): {
            "state": PersonalDataForm.first_name,
            "message": BOT_ANSWERS.first_name.value,
            "keyboard": CANCEL_KEYBOARD,
        },
        BOT_ANSWERS.try_again.value.casefold(): {
            "state": PersonalDataForm.first_name,
            "message": BOT_ANSWERS.first_name.value,
            "keyboard": CANCEL_KEYBOARD,
        },
    }
    if (
        not hasattr(message.text, "casefold")
        or not message.text.casefold() in responses
    ):
        await message.reply(
            BOT_ANSWERS.choose_correct_option.value,
            reply_markup=YES_NO_KEYBOARD,
        )
        return

    response = responses[message.text.casefold()]
    await state.set_state(response["state"])
    await message.answer(
        response["message"], reply_markup=response.get("keyboard")
    )


@router.message(PersonalDataForm.first_name)
async def process_name(message: Message, state: FSMContext) -> None:
    if not await check_message(
        message,
        BOT_ANSWERS.enter_correct_value.value,
    ):
        return
    await state.update_data(first_name=message.text)
    await state.set_state(PersonalDataForm.second_name)
    await message.answer(BOT_ANSWERS.second_name.value)


@router.message(PersonalDataForm.second_name)
async def process_name(message: Message, state: FSMContext) -> None:
    if not await check_message(
        message,
        BOT_ANSWERS.enter_correct_value.value,
    ):
        return
    await state.update_data(second_name=message.text)
    await state.set_state(PersonalDataForm.surname)
    await message.answer(BOT_ANSWERS.surname.value)


@router.message(PersonalDataForm.surname)
async def process_surname(message: Message, state: FSMContext) -> None:
    if not await check_message(
        message,
        BOT_ANSWERS.enter_correct_value.value,
    ):
        return
    await state.update_data(surname=message.text)
    await state.set_state(PersonalDataForm.email)
    await message.answer(
        BOT_ANSWERS.email.value,
    )


@router.message(PersonalDataForm.email)
async def process_email(message: Message, state: FSMContext, bot: Bot) -> None:
    if not await check_message(
        message,
        BOT_ANSWERS.enter_correct_value.value,
    ):
        return
    await state.update_data(email=message.text)
    await state.set_state(PersonalDataForm.phone_number)
    await message.answer(
        BOT_ANSWERS.phone_number.value, reply_markup=SEND_CONTACT_KEYBOARD
    )


@router.message(
    PersonalDataForm.phone_number,
)
async def process_phone_number(
    message: Message, state: FSMContext, access: str = None
) -> None:
    if not access:
        await state.set_state(InformationAboutShelter.main_interaction)
        await message.answer(BOT_ANSWERS.something_went_wrong.value)
        return
    if not message.contact and not await check_message(
        message,
        BOT_ANSWERS.enter_correct_value.value,
    ):
        return
    if message.contact:
        data = await state.update_data(
            phone_number=message.contact.phone_number
        )
    else:
        data = await state.update_data(phone_number=message.text)
    user = {
        "name": data["first_name"],
        "second_name": data["second_name"],
        "surname": data["surname"],
        "email": data["email"],
        "phone_number": data["phone_number"],
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
    if user_db.get("details") == "Backend validation error":
        answer = "Ошибка валидации:\n"
        for key, value in user_db.items():
            if key != "details":
                answer += f"{' ,'.join(value)}\n"
        await state.set_state(PersonalDataForm.permission)
        await message.answer(answer, reply_markup=TRY_AGAIN_KEYBOARD)
        return
    await state.clear()
    await state.set_state(InformationAboutShelter.main_interaction)
    await send_main_interaction_buttons(
        message, BOT_ANSWERS.registration_message.value
    )


@router.message(InformationAboutShelter.main_interaction)
async def process_main_interaction(
    message: Message, state: FSMContext
) -> None:
    responses = {
        BOT_ANSWERS.unique_question.value.casefold(): {
            "state": InformationAboutShelter.unique_question,
            "message": BOT_ANSWERS.enter_unique_question.value,
            "keyboard": CANCEL_KEYBOARD,
        },
        BOT_ANSWERS.shelter.value.casefold(): {
            "state": InformationAboutShelter.questions,
            "message": BOT_ANSWERS.questions_title.value,
            "keyboard": FAQ_INFO_CANCEL_KEYBOARD,
        },
        BOT_ANSWERS.cancel.value.casefold(): {
            "state": InformationAboutShelter.main_interaction,
            "message": "Отменять нечего, мы и так в самом начале :)",
            "keyboard": MAIN_INTERACTION_KEYBOARD,
        },
    }
    if (
        not hasattr(message.text, "casefold")
        or not message.text.casefold() in responses
    ):
        await message.reply(
            BOT_ANSWERS.choose_correct_option.value,
            reply_markup=MAIN_INTERACTION_KEYBOARD,
        )
        return

    response = responses[message.text.casefold()]
    await state.set_state(response["state"])
    await message.answer(
        response["message"], reply_markup=response.get("keyboard")
    )


@router.message(
    InformationAboutShelter.questions,
)
async def process_questions(
    message: Message,
    bot: Bot,
    shelter_information: InformationSchema = {},
) -> None:
    category_mapping = {
        BOT_ANSWERS.faq.value.casefold(): "faq",
        BOT_ANSWERS.info.value.casefold(): "info",
        BOT_ANSWERS.needs.value.casefold(): "needs",
    }
    if (
        not hasattr(message.text, "casefold")
        or not message.text.casefold() in category_mapping
    ):
        await message.reply(
            BOT_ANSWERS.choose_correct_category.value,
            reply_markup=FAQ_INFO_CANCEL_KEYBOARD,
        )
        return

    category = message.text.casefold()

    await delete_inline_keyboard(message, bot)
    await send_paginated_data(
        message, shelter_information, category_mapping[category], 0
    )


@router.message(InformationAboutShelter.unique_question)
async def process_unique_question(
    message: Message, state: FSMContext, access: str = None
) -> None:
    if not access:
        await state.set_state(InformationAboutShelter.main_interaction)
        await message.answer(BOT_ANSWERS.something_went_wrong.value)
        return
    if not await check_message(
        message, BOT_ANSWERS.enter_correct_question.value
    ):
        return

    question = {"text": message.text, "owner": message.chat.id}
    question_db = await add_unique_question(question, access)
    if question_db is None:
        await state.set_state(InformationAboutShelter.main_interaction)
        await message.answer(BOT_ANSWERS.question_creation_error.value)
        return
    await state.set_state(InformationAboutShelter.main_interaction)
    await message.answer(
        BOT_ANSWERS.unique_question_reply.value,
        reply_markup=MAIN_INTERACTION_KEYBOARD,
    )


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


@router.callback_query(
    (
        F.data.contains("faq_")
        | F.data.contains("info_")
        | F.data.contains("needs_")
    )
    & ~F.data.contains("page_")
)
async def process_faq_callback(
    callback_query: CallbackQuery,
    shelter_information: InformationSchema,
    bot: Bot,
) -> None:
    data, quiestion_id = callback_query.data.split("_")
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


@router.callback_query(F.data.contains("page_"))
async def process_page_callback(
    callback_query: CallbackQuery, shelter_information: InformationSchema
) -> None:
    key, _, page = callback_query.data.split("_")
    await send_paginated_data(
        callback_query.message, shelter_information, key, int(page)
    )
