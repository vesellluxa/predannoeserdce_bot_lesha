from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from constants import BOT_ANSWERS
from keyboards import (
    FAQ_INFO_CANCEL_KEYBOARD,
    MAIN_INTERACTION_KEYBOARD,
    create_animals_keyboard,
    create_donation_keyboard,
)
from schemas.schemas import InformationSchema
from states.states import InformationAboutShelter
from utils.helpers import (
    check_message,
    delete_inline_keyboard,
    send_paginated_data,
)
from utils.services import add_unique_question


async def process_main_interaction(
    message: Message,
    state: FSMContext,
    shelter_information: InformationSchema,
) -> None:
    responses = {
        BOT_ANSWERS.shelter.value.casefold(): {
            "state": InformationAboutShelter.questions,
            "message": BOT_ANSWERS.questions_title.value,
            "keyboard": FAQ_INFO_CANCEL_KEYBOARD,
        },
        BOT_ANSWERS.animals.value.casefold(): {
            "state": InformationAboutShelter.main_interaction,
            "message": BOT_ANSWERS.animals_title.value,
            "keyboard": create_animals_keyboard(shelter_information),
        },
        BOT_ANSWERS.monetary_aid.value.casefold(): {
            "state": InformationAboutShelter.main_interaction,
            "message": BOT_ANSWERS.monetary_aid_title.value,
            "keyboard": create_donation_keyboard(shelter_information),
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
    if question_db.get("details") == "Question contains forbidden words":
        await state.set_state(InformationAboutShelter.main_interaction)
        await message.answer(
            BOT_ANSWERS.question_validation_error.value,
            reply_markup=MAIN_INTERACTION_KEYBOARD,
        )
        return
    await state.set_state(InformationAboutShelter.main_interaction)
    await message.answer(
        BOT_ANSWERS.unique_question_reply.value,
        reply_markup=MAIN_INTERACTION_KEYBOARD,
    )
