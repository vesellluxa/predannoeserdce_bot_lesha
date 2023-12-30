from aiogram.fsm.state import State, StatesGroup


class PersonalDataForm(StatesGroup):
    permission = State()
    update_data = State()
    name = State()
    email = State()
    phone_number = State()


class InformationAboutShelter(StatesGroup):
    main_interaction = State()
    questions = State()
    unique_question = State()
