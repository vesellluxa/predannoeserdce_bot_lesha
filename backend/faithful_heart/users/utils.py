from datetime import datetime

from openpyxl.workbook.workbook import Workbook

from users.models import TelegramUser
from faithful_heart import constants
from faithful_heart.settings import MEDIA_ROOT

HEADERS = [
    "Имя",
    "Фамилия",
    "Отчество",
    "Номер телефона",
    "Username в telegram",
    "Email",
]


def export_users_excel():
    """
    Создание файла excel с данными пользователей.
    """
    workbook = Workbook()
    sheet = workbook.active
    sheet_column_dimensions = {
        "A": 10,
        "B": 15,
        "C": 18,
        "D": 18,
        "E": 18,
        "F": 18,
    }
    for column, width in sheet_column_dimensions.items():
        sheet.column_dimensions[column].width = width
    sheet.append(HEADERS)

    users = TelegramUser.objects.filter(consent_to_save_personal_data=True)
    for user in users:
        sheet.append(
            [
                user.name,
                user.surname,
                user.middle_name,
                user.phone_number,
                user.username,
                user.email,
            ]
        )

    date_now_formatted = datetime.now().strftime(constants.DATETIME_FORMAT)
    path_to_file = f"{MEDIA_ROOT}/Пользователи_{date_now_formatted}.xlsx"
    workbook.save(path_to_file)
    return path_to_file
