from aiogram.fsm.state import State, StatesGroup


class PersonalDataForm(StatesGroup):
    permission = State()
    update_data = State()
    first_name = State()
    second_name = State()
    surname = State()
    email = State()
    phone_number = State()


class InformationAboutShelter(StatesGroup):
    main_interaction = State()
    questions = State()
    unique_question = State()
