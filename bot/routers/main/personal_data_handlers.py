from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from constants import BOT_ANSWERS
from keyboards import (
    CANCEL_KEYBOARD,
    DATA_UPDATE_KEYBOARD,
    MAIN_INTERACTION_KEYBOARD,
    PERSONAL_DATA_CONSENT_KEYBOARD,
    SEND_CONTACT_KEYBOARD,
    TRY_AGAIN_KEYBOARD,
    YES_NO_KEYBOARD,
    send_main_interaction_buttons,
)
from states.states import InformationAboutShelter, PersonalDataForm
from utils.helpers import check_message, validate_email, validate_name
from utils.services import patch_user


async def process_update(
    message: Message, state: FSMContext, access: str = None
) -> None:
    responses = {
        BOT_ANSWERS.back.value.casefold(): {
            "state": InformationAboutShelter.main_interaction,
            "message": BOT_ANSWERS.data_back_message.value,
            "keyboard": MAIN_INTERACTION_KEYBOARD,
        },
        BOT_ANSWERS.update.value.casefold(): {
            "state": PersonalDataForm.name,
            "message": BOT_ANSWERS.personal_data_consent.value,
            "keyboard": PERSONAL_DATA_CONSENT_KEYBOARD,
        },
        BOT_ANSWERS.delete.value.casefold(): {},
    }
    if (
        not hasattr(message.text, "casefold")
        or not message.text.casefold() in responses
    ):
        await message.reply(
            BOT_ANSWERS.choose_correct_option.value,
            reply_markup=DATA_UPDATE_KEYBOARD,
        )
        return
    if message.text.casefold() == BOT_ANSWERS.delete.value.casefold():
        if not access:
            await state.set_state(InformationAboutShelter.main_interaction)
            await message.answer(BOT_ANSWERS.something_went_wrong.value)
            return
        user = {
            "name": "",
            "middle_name": "",
            "surname": "",
            "phone_number": None,
            "email": None,
            "chat_id": message.chat.id,
            "username": message.chat.username.lower(),
            "consent_to_save_personal_data": False,
        }
        user_db = await patch_user(user, access)
        if user_db is None:
            await state.set_state(InformationAboutShelter.main_interaction)
            await message.answer(
                BOT_ANSWERS.update_error.value,
                reply_markup=MAIN_INTERACTION_KEYBOARD,
            )
            return
        if user_db.get("details") == "Backend error":
            answer = "Ошибка:\n"
            for key, value in user_db.items():
                if key != "details":
                    answer += f"{' ,'.join(value)}\n"
            await state.set_state(PersonalDataForm.update_data)
            await message.answer(answer, reply_markup=DATA_UPDATE_KEYBOARD)
            return
        await state.set_state(InformationAboutShelter.main_interaction)
        await message.answer(
            "Ваши данные удалены", reply_markup=MAIN_INTERACTION_KEYBOARD
        )
        return
    response = responses[message.text.casefold()]
    await state.set_state(response["state"])
    await message.answer(
        response["message"], reply_markup=response.get("keyboard")
    )


async def process_permission(message: Message, state: FSMContext) -> None:
    responses = {
        BOT_ANSWERS.no.value.casefold(): {
            "state": InformationAboutShelter.main_interaction,
            "message": BOT_ANSWERS.permission.value,
            "keyboard": MAIN_INTERACTION_KEYBOARD,
        },
        BOT_ANSWERS.yes.value.casefold(): {
            "state": PersonalDataForm.permission,
            "message": BOT_ANSWERS.personal_data_consent.value,
            "keyboard": PERSONAL_DATA_CONSENT_KEYBOARD,
        },
        BOT_ANSWERS.try_again.value.casefold(): {
            "state": PersonalDataForm.name,
            "message": BOT_ANSWERS.name.value,
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


async def process_name(message: Message, state: FSMContext) -> None:
    if not await check_message(
        message,
        BOT_ANSWERS.enter_correct_value.value,
    ):
        return
    validated_name = validate_name(message.text)
    if not validated_name:
        await message.answer(
            BOT_ANSWERS.enter_correct_value.value
            + "\n"
            + message.text.capitalize()
            + " не является корректным именем.",
            reply_markup=CANCEL_KEYBOARD,
        )
        return
    await state.update_data(name=validated_name)
    await state.set_state(PersonalDataForm.email)
    await message.answer(BOT_ANSWERS.email.value)


async def process_email(message: Message, state: FSMContext) -> None:
    if not await check_message(
        message,
        BOT_ANSWERS.enter_correct_value.value,
    ):
        return
    if not validate_email(message.text):
        await message.answer(
            BOT_ANSWERS.enter_correct_value.value
            + "\n"
            + message.text
            + " не является корректным email.",
            reply_markup=CANCEL_KEYBOARD,
        )
        return
    await state.update_data(email=message.text)
    await state.set_state(PersonalDataForm.phone_number)
    await message.answer(
        BOT_ANSWERS.phone_number.value, reply_markup=SEND_CONTACT_KEYBOARD
    )


async def process_phone_number(
    message: Message, state: FSMContext, access: str = None
) -> None:
    if not access:
        await state.set_state(InformationAboutShelter.main_interaction)
        await message.answer(BOT_ANSWERS.something_went_wrong.value)
        return
    if not message.contact and not await check_message(
        message, BOT_ANSWERS.contact_button.value, SEND_CONTACT_KEYBOARD
    ):
        return
    if not message.contact:
        await message.answer(
            BOT_ANSWERS.contact_button.value,
            reply_markup=SEND_CONTACT_KEYBOARD,
        )
        return
    if message.contact:
        data = await state.update_data(
            phone_number=message.contact.phone_number
        )
    else:
        data = await state.update_data(phone_number=message.text)
    name = data.get("name").split(" ")
    user = {
        "surname": name[0],
        "name": name[1] if len(name) > 1 else "",
        "middle_name": name[2] if len(name) > 2 else "",
        "email": data["email"],
        "phone_number": data["phone_number"],
        "chat_id": message.chat.id,
        "username": message.chat.username.lower(),
        "consent_to_save_personal_data": True,
    }
    user_db = await patch_user(user, access)
    if user_db is None:
        await state.set_state(PersonalDataForm.permission)
        await message.answer(
            BOT_ANSWERS.update_error.value, reply_markup=TRY_AGAIN_KEYBOARD
        )
        return
    if user_db.get("details") == "Backend error":
        answer = "Ошибка:\n"
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
