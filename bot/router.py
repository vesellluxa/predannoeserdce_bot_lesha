import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardRemove,
)
from constants import BOT_ANSWERS, PAGINATION
from helpers import Question, add_unique_question, add_user_to_db, get_shelter_info
from keyboards import (
    CANCEL_KEYBOARD,
    FAQ_UNIQUE_CANCEL_KEYBOARD,
    TRY_AGAIN_KEYBOARD,
    YES_NO_KEYBOARD,
    send_main_interaction_buttons,
)
from middelware import QuestionsMiddelware

router = Router()
router.message.middleware(QuestionsMiddelware())
router.callback_query.middleware(QuestionsMiddelware())


class PersonalDataForm(StatesGroup):
    permission = State()
    name = State()
    surname = State()
    email = State()
    phone = State()


class InformationAboutShelter(StatesGroup):
    main_interaction = State()
    questions = State()
    unique_question = State()


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    """
    Handles the start command.

    Args:
      message (Message): The incoming message.
      state (FSMContext): The state of the conversation.

    Returns:
      None
    """
    logging.info("Start command received")
    await state.set_state(PersonalDataForm.permission)
    await message.answer(BOT_ANSWERS.greeting.value, reply_markup=YES_NO_KEYBOARD)


@router.message(
    PersonalDataForm.name, F.text.casefold() == BOT_ANSWERS.cancel.value.casefold()
)
@router.message(
    PersonalDataForm.surname, F.text.casefold() == BOT_ANSWERS.cancel.value.casefold()
)
@router.message(
    PersonalDataForm.email, F.text.casefold() == BOT_ANSWERS.cancel.value.casefold()
)
@router.message(
    PersonalDataForm.phone, F.text.casefold() == BOT_ANSWERS.cancel.value.casefold()
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
    """
    Handles the "cancel" messages for the both states.

    Args:
      message (Message): The incoming message.
      state (FSMContext): The state of the conversation.

    Returns:
      None
    """
    await state.set_state(PersonalDataForm.permission)
    await message.answer(BOT_ANSWERS.greeting.value, reply_markup=YES_NO_KEYBOARD)


@router.message(
    PersonalDataForm.permission,
    (F.text.casefold() == BOT_ANSWERS.no.value.casefold())
    | (F.text.casefold() == BOT_ANSWERS.yes.value.casefold())
    | (F.text.casefold() == BOT_ANSWERS.try_again.value.casefold()),
)
async def process_permission(message: Message, state: FSMContext) -> None:
    """
    Processes the user's response to the permission question.

    Args:
      message (Message): The incoming message from the user.
      state (FSMContext): The state of the conversation.

    Returns:
      None
    """
    logging.info("process_permission")
    current_state = await state.get_state()
    logging.info(current_state)
    if message.text.casefold() == BOT_ANSWERS.no.value.casefold():
        await state.set_state(InformationAboutShelter.main_interaction)
        await send_main_interaction_buttons(message, BOT_ANSWERS.permission.value)
    else:
        await state.set_state(PersonalDataForm.name)
        await message.answer(
            BOT_ANSWERS.name.value,
            reply_markup=CANCEL_KEYBOARD,
        )


@router.message(PersonalDataForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    """
    Processes the user's name and update the state.

    Args:
      message (Message): The incoming message from the user.
      state (FSMContext): The current state of the conversation.

    Returns:
      None
    """
    logging.info("process_name")
    await state.update_data(name=message.text)
    await state.set_state(PersonalDataForm.surname)
    await message.answer(BOT_ANSWERS.surname.value)


@router.message(PersonalDataForm.surname)
async def process_surname(message: Message, state: FSMContext) -> None:
    """
    Processes the user's surname and update the state.

    Args:
      message (Message): The incoming message from the user.
      state (FSMContext): The current state of the conversation.

    Returns:
      None
    """
    logging.info("process_surname")
    await state.update_data(surname=message.text)
    await state.set_state(PersonalDataForm.email)
    await message.answer(
        BOT_ANSWERS.email.value,
    )


@router.message(PersonalDataForm.email)
async def process_email(message: Message, state: FSMContext) -> None:
    """
    Processes the email entered by the user.

    Args:
      message (Message): The message object containing the user's input.
      state (FSMContext): The state machine context.

    Returns:
      None
    """
    logging.info("process_email")
    await state.update_data(email=message.text)
    await state.set_state(PersonalDataForm.phone)
    await message.answer(BOT_ANSWERS.phone.value)


@router.message(PersonalDataForm.phone)
async def process_phone(message: Message, state: FSMContext) -> None:
    """
    Processes the phone number entered by the user and updates the state data.
    Sends the request to add the user to the database and clears the state.
    Sets the state to the main interaction state and sends the main interaction buttons.

    Args:
      message (Message): The message object containing the user's input.
      state (FSMContext): The state machine context object.

    Returns:
      None
    """
    logging.info("process_phone")
    data = await state.update_data(phone=message.text)
    user = {
        "name": data["name"],
        "surname": data["surname"],
        "email": data["email"],
        "phone": data["phone"],
        "chat_id": message.chat.id,
        "username": message.chat.username,
    }
    user = await add_user_to_db(user)
    logging.info(user)
    if user is None:
        await state.set_state(PersonalDataForm.permission)
        await message.answer(
            BOT_ANSWERS.validation_error.value, reply_markup=TRY_AGAIN_KEYBOARD
        )
        return
    await state.clear()
    await state.set_state(InformationAboutShelter.main_interaction)
    await send_main_interaction_buttons(message, BOT_ANSWERS.registration_message.value)


@router.message(
    InformationAboutShelter.main_interaction,
    (
        (F.text.casefold() == BOT_ANSWERS.questions.value.casefold())
        | (F.text.casefold() == BOT_ANSWERS.shelter.value.casefold())
    ),
)
async def process_main_interaction(message: Message) -> None:
    """
    Processes the main interaction with the bot.

    Args:
      message (Message): The incoming message.

    Returns:
      None
    """
    logging.info("process_main_interaction")
    if message.text.casefold() == BOT_ANSWERS.questions.value.casefold():
        await message.answer(
            BOT_ANSWERS.questions_title.value,
            reply_markup=FAQ_UNIQUE_CANCEL_KEYBOARD,
        )
    else:
        shelter_info = await get_shelter_info()
        await message.answer(
            shelter_info,
            reply_markup=FAQ_UNIQUE_CANCEL_KEYBOARD,
        )


@router.message(
    InformationAboutShelter.main_interaction,
    (
        (F.text.casefold() == BOT_ANSWERS.faq.value.casefold())
        | (F.text.casefold() == BOT_ANSWERS.unique_question.value.casefold())
    ),
)
async def process_questions(
    message: Message, questions: dict[int, Question], state: FSMContext
) -> None:
    """
    Processes the interaction with the bot for the questions.
    Sends back paginated faq questions or allows user to ask a unique question.

    Args:
      message (Message): The incoming message.
      questions (dict[int, Question]): The dictionary of questions.
      state (FSMContext): The state of the conversation.

    Returns:
      None
    """
    logging.info("process_questions")
    if message.text.casefold() == BOT_ANSWERS.faq.value.casefold():
        await send_questions_page(message, questions, 0)
    elif message.text.casefold() == BOT_ANSWERS.unique_question.value.casefold():
        await state.set_state(InformationAboutShelter.unique_question)
        await message.answer(BOT_ANSWERS.enter_unique_question.value)


@router.message(InformationAboutShelter.unique_question)
async def process_unique_question(message: Message, state: FSMContext) -> None:
    """
    Processes the unique question entered by the user.
    Adds the question to the database and sends a reply.

    Args:
      message (Message): The incoming message.
      state (FSMContext): The state of the conversation.

    Returns:
      None
    """
    logging.info("process_unique_question")
    question = {
        "question": message.text,
        "username": message.chat.username,
        "chat_id": message.chat.id,
    }
    await add_unique_question(question)
    await state.set_state(InformationAboutShelter.main_interaction)
    await message.answer(BOT_ANSWERS.unique_question_reply.value)


async def send_questions_page(
    message: Message, questions: dict[int, Question], page: int
) -> None:
    """
    Sends the paginated questions to the user.

    Args:
      message (Message): The incoming message.
      questions (dict[int, Question]): The dictionary of questions.
      page (int): The page number.

    Returns:
      None
    """
    logging.info("send_questions_page")
    # It is better to use a list of indexes, as the indexes in the database may not be consistent if records are deleted
    indexes = list(questions)
    start_idx = page * PAGINATION
    end_idx = start_idx + PAGINATION
    buttons = [
        [
            InlineKeyboardButton(
                text=questions[indexes[i]].question,
                callback_data=f"faq_{indexes[i]}",
            )
        ]
        for i in range(
            start_idx, end_idx if end_idx < len(questions) else len(questions)
        )
    ]
    if page > 0:
        buttons.append(
            [InlineKeyboardButton(text="◀️ Назад", callback_data=f"page_{page - 1}")]
        )
    if end_idx < len(questions):
        buttons.append(
            [InlineKeyboardButton(text="Вперед ▶️", callback_data=f"page_{page + 1}")]
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


@router.callback_query(F.data.contains("faq_"))
async def process_faq_callback(
    callback_query: CallbackQuery, questions: dict[int, Question]
) -> None:
    """
    Process callback query for FAQ questions.

    Args:
      callback_query (CallbackQuery): The callback query object.
      questions (dict[int, Question]): The dictionary of questions.

    Returns:
      None
    """
    logging.info("process_faq_callback")
    quiestion_id = int(callback_query.data.split("_")[1])
    question = questions.get(quiestion_id)
    if question is None:
        await callback_query.answer("Вопрос не найден")
        return
    await callback_query.message.answer(question.answer)


@router.callback_query(F.data.contains("page_"))
async def process_page_callback(
    callback_query: CallbackQuery, questions: dict[int, Question]
) -> None:
    """
    Process callback query for pagination.

    Args:
      callback_query (CallbackQuery): The callback query object.
      questions (dict[int, Question]): The dictionary of questions.

    Returns:
      None
    """
    logging.info("process_page_callback")
    page = int(callback_query.data.split("_")[1])
    await send_questions_page(callback_query.message, questions, page)
