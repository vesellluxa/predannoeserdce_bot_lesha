import logging

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from constants import BOT_ANSWERS
from keyboards import YES_NO_KEYBOARD, send_main_interaction_buttons
from states.states import InformationAboutShelter, PersonalDataForm
from utils.helpers import delete_inline_keyboard
from utils.services import add_user_to_db, check_user_status


async def command_cancel(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    await state.set_state(InformationAboutShelter.main_interaction)
    await delete_inline_keyboard(message, bot)
    await send_main_interaction_buttons(
        message, BOT_ANSWERS.greeting_full_data.value
    )


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
        "username": message.chat.username.lower(),
    }
    user_db = await add_user_to_db(user, access)
    logging.info(f"User added to DB: {user_db}")
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
