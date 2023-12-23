import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.exceptions import TelegramBadRequest

from constants import BOT_ANSWERS, PAGINATION
from helpers import (
    Question,
)
from middelwares import QuestionsMiddelware
from keyboards import (
    YES_NO_KEYBOARD,
    FAQ_UNIQUE_CANCEL_KEYBOARD,
    send_main_interaction_buttons,
)

router = Router()
router.message.middleware(QuestionsMiddelware())
router.callback_query.middleware(QuestionsMiddelware())


class PersonalDataForm(StatesGroup):
    permission = State()
    name = State()
    email = State()
    phone_number = State()


class InformationAboutShelter(StatesGroup):
    main_interaction = State()
    questions = State()


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    """
    Handle the start command.

    Args:
      message (Message): The incoming message.
      state (FSMContext): The state of the conversation.

    Returns:
      None
    """
    logging.info("Start command received")
    await state.set_state(PersonalDataForm.permission)
    await message.answer(
        BOT_ANSWERS.greeting.value, reply_markup=YES_NO_KEYBOARD
    )


@router.message(
    PersonalDataForm.permission,
    (
        (F.text.casefold() == BOT_ANSWERS.no.value.casefold())
        | (F.text.casefold() == BOT_ANSWERS.yes.value.casefold())
    ),
)
async def process_permission(message: Message, state: FSMContext) -> None:
    """
    Process the user's response to the permission question.

    Args:
      message (Message): The incoming message from the user.
      state (FSMContext): The state of the conversation.

    Returns:
      None
    """
    logging.info("process_permission")
    if message.text.casefold() == BOT_ANSWERS.no.value.casefold():
        await state.set_state(InformationAboutShelter.main_interaction)
        await send_main_interaction_buttons(
            message, BOT_ANSWERS.permission.value
        )
    else:
        await state.set_state(PersonalDataForm.name)
        await message.answer(
            BOT_ANSWERS.first_name.value,
            reply_markup=ReplyKeyboardRemove(),
        )


@router.message(PersonalDataForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    """
    Process the user's name and update the state.

    Args:
      message (Message): The incoming message from the user.
      state (FSMContext): The current state of the conversation.

    Returns:
      None
    """
    logging.info("process_name")
    await state.update_data(name=message.text)
    await state.set_state(PersonalDataForm.email)
    await message.answer(
        BOT_ANSWERS.email.value,
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(PersonalDataForm.email)
async def process_email(message: Message, state: FSMContext) -> None:
    """
    Process the email entered by the user.

    Args:
      message (Message): The message object containing the user's input.
      state (FSMContext): The state machine context.

    Returns:
      None
    """
    logging.info("process_email")
    await state.update_data(email=message.text)
    await state.set_state(PersonalDataForm.phone_number)
    await message.answer(BOT_ANSWERS.phone_number.value)


@router.message(PersonalDataForm.phone_number)
async def process_phone_number(message: Message, state: FSMContext) -> None:
    """
    Processes the phone number entered by the user and updates the state data.
    Sends a message with the user's personal information and clears the state.
    Sets the state to the main interaction state and sends the main interaction buttons.

    Args:
      message (Message): The message object containing the user's input.
      state (FSMContext): The state machine context object.

    Returns:
      None
    """
    logging.info("process_phone_number")
    await state.update_data(phone_number=message.text)
    data = await state.update_data(language=message.text)
    text = f"Ваше ФИО: {data['name']}\n"
    text += f"Ваш email: {data['email']}\n"
    text += f"Ваш номер телефона: {data['phone_number']}\n"
    await message.answer(text)
    await state.clear()
    await state.set_state(InformationAboutShelter.main_interaction)
    await send_main_interaction_buttons(
        message, BOT_ANSWERS.registration_message.value
    )


@router.message(
    InformationAboutShelter.main_interaction,
    (
        (F.text.casefold() == BOT_ANSWERS.questions.value.casefold())
        | (F.text.casefold() == BOT_ANSWERS.shelter.value.casefold())
    ),
)
async def process_main_interaction(
    message: Message, state: FSMContext
) -> None:
    logging.info("process_main_interaction")
    if message.text.casefold() == BOT_ANSWERS.questions.value.casefold():
        await message.answer(
            BOT_ANSWERS.questions_title.value,
            reply_markup=FAQ_UNIQUE_CANCEL_KEYBOARD,
        )
    else:
        await message.answer(BOT_ANSWERS.shelter_info.value)


@router.message(
    InformationAboutShelter.main_interaction,
    F.text.casefold() == BOT_ANSWERS.faq.value.casefold(),
)
async def process_faq(
    message: Message, state: FSMContext, questions: dict[int, Question]
) -> None:
    logging.info("process_faq")
    await send_questions_page(message, questions, 0)


async def send_questions_page(
    message: Message, questions: dict[int, Question], page: int
) -> None:
    logging.info("send_questions_page")
    start_idx = page * PAGINATION + 1
    end_idx = start_idx + PAGINATION
    buttons = [
        [
            InlineKeyboardButton(
                text=questions[i].question,
                callback_data=f"faq_{i}",
            )
        ]
        for i in range(
            start_idx, end_idx if end_idx < len(questions) else len(questions)
        )
    ]
    if page > 0:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="◀️ Назад", callback_data=f"page_{page - 1}"
                )
            ]
        )
    if end_idx < len(questions):
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Вперед ▶️", callback_data=f"page_{page + 1}"
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
            BOT_ANSWERS.questions_title.value,
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

    Returns:
      None
    """
    logging.info("process_page_callback")
    page = int(callback_query.data.split("_")[1])
    await send_questions_page(callback_query.message, questions, page)


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )
