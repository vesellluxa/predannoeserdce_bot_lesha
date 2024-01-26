import os

import dotenv

dotenv.load_dotenv()

USERNAME_MIN_LENGTH = 5
USERNAME_MAX_LENGTH = 32
NAME_REGEX = r"^[а-яА-ЯёЁ-]+$"
NAME_MIN_LENGTH = 1
NAME_MAX_LENGTH = 64
SURNAME_MAX_LENGTH = 64
SURNAME_MIN_LENGHT = 1
PHONE_NUMBER_REGEX = r"^[0-9]"
PHONE_NUMBER_LENGTH = 11
FAQ_MAX_LENGTH = 1024
CHAT_ID_MIN_LENGTH = 6
CHAT_ID_MAX_LENGTH = 15
PROD_URL = os.getenv("PROD_URL")
DATETIME_FORMAT = "%Y%m%d"
CHAT_ID_REGEX = r"\d"
TELEGRAM_USERNAME_REGEX = r"([a-z]|\d|[_])"
CATEGORY_MAX_LENGTH = 24
NOTIFICATION_MAX_LENGTH = 1024

ACCESS_TOKEN_LIFETIME = 5
REFRESH_TOKEN_LIFETIME = 1
SLIDING_TOKEN_LIFETIME = 5
SLIDING_TOKEN_REFRESH_LIFETIME = 1

USERNAME_REGEX_VALIDATOR_ERROR_TEXT = ("Юзернейм должен состоять "
                                       "только из букв английского алфавита "
                                       "и/или цифр, а также может "
                                       "иметь символ '_'."
                                       "Всего не менее 5 и "
                                       "не более 32 знаков.")
NAME_REGEX_VALIDATOR_ERROR_TEXT = ("Имя должно состоять только"
                                   " из букв русского алфавита "
                                   "и быть не более 64 знаков.")
SURNAME_REGEX_VALIDATOR_ERROR_TEXT = ("Фамилия должна состоять только"
                                      " из букв русского алфавита и "
                                      "быть не более 64 знаков.")
PATRONYMIC_REGEX_VALIDATOR_ERROR_TEXT = ("Отчество должно состоять только"
                                         " из букв русского алфавита и "
                                         "быть не более 64 знаков.")
PHONE_NUMBER_REGEX_VALIDATOR_ERROR_TEXT = ("Номер телефона должен состоять "
                                           "только из цифр и не превышать "
                                           "12 знаков.")
CHAT_ID_REGEX_VALIDATOR_ERROR_TEXT = ("Chat ID должен состоять только из цифр"
                                      " и быть не менее 6 и не более "
                                      "15 знаков.")

FAQ = ("FAQ", "Часто Задаваемые Вопросы")
SHELTER_INFO = ("Shelter_Info", "Узнать больше о приюте")
NEEDS = ("Needs", "Нужды приюта")
DONATIONS = ("Donations", "Сделать пожертвование")
LIST_ANIMALS = ("List_Animals", "Список животных")

URL_TO_QUESTION = PROD_URL + "/admin/questions/uniquequestion/{}/change/"
ADMIN_NOTIFICATION = "Поступил новый вопрос. Ссылка: {}"
USER_NOTIFICATION = ("Поступил ответ на ваш вопрос: \n"
                     "Вопрос: {}: \n"
                     "Ответ: {}")
