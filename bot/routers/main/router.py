from aiogram import F, Router
from aiogram.filters import CommandStart
from constants import BOT_ANSWERS
from states.states import InformationAboutShelter, PersonalDataForm

from .callbacks import (
    process_faq_callback,
    process_page_callback,
    process_personal_data_consent,
    process_back_to_questions_callback
)
from .commands_handlers import command_cancel, command_data, command_start
from .main_interaction_handlers import (
    process_main_interaction,
    process_questions,
    process_unique_question,
)
from .middleware import FetchingMiddleware, TokenMiddleware
from .personal_data_handlers import (
    process_email,
    process_name,
    process_permission,
    process_phone_number,
    process_update,
)

router = Router()

router.message.middleware(TokenMiddleware())
router.message.middleware(FetchingMiddleware())

router.callback_query.middleware(FetchingMiddleware())
router.callback_query.middleware(TokenMiddleware())

router.message.register(command_start, CommandStart())
router.message.register(
    command_cancel,
    (
        (F.text.casefold() == BOT_ANSWERS.cancel.value.casefold())
        | (F.text.casefold() == "/cancel")
    ),
)
router.message.register(command_data, F.text.casefold() == "/data")
router.message.register(process_update, PersonalDataForm.update_data)
router.message.register(process_permission, PersonalDataForm.permission)
router.message.register(process_name, PersonalDataForm.name)
router.message.register(process_email, PersonalDataForm.email)
router.message.register(process_phone_number, PersonalDataForm.phone_number)

router.message.register(
    process_main_interaction, InformationAboutShelter.main_interaction
)
router.message.register(process_questions, InformationAboutShelter.questions)
router.message.register(
    process_unique_question, InformationAboutShelter.unique_question
)

router.callback_query.register(
    process_faq_callback,
    (
        F.data.contains("faq_")
        | F.data.contains("info_")
        | F.data.contains("needs_")
    )
    & ~F.data.contains("page_"),
)
router.callback_query.register(process_back_to_questions_callback, F.data.contains("back_toquestions"))
router.callback_query.register(process_page_callback, F.data.contains("page_"))
router.callback_query.register(
    process_personal_data_consent, F.data.contains("personal_data_consent_")
)
