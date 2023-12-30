from datetime import datetime

from django.core.mail import send_mail
from openpyxl import Workbook

from faithful_heart import constants
from faithful_heart.settings import MEDIA_ROOT
from users.models import User


def export_users_excel(users):
    """
    Создание файла excel с данными пользователей.
    """
    date_now = datetime.now()
    date_now_formatted = date_now.strftime(constants.DATETIME_FORMAT)
    workbook = Workbook()
    sheet = workbook.active
    sheet.column_dimensions["A"].width = 10
    sheet.column_dimensions["B"].width = 15
    sheet.column_dimensions["C"].width = 18
    sheet.column_dimensions["D"].width = 18
    sheet.column_dimensions["E"].width = 18
    sheet.column_dimensions["F"].width = 18
    headers = [
        "Name",
        "Surname",
        "Phone Number",
        "Username",
        "Chat_id",
        "Email",
    ]
    sheet.append(headers)
    for user in users:
        sheet.append(
            [
                user.name,
                user.surname,
                user.phone_number,
                user.username,
                user.chat_id,
                user.email,
            ]
        )
    workbook.save(f"{MEDIA_ROOT}/Пользователи_{date_now_formatted}.xlsx")


def send_email_to_admin(question):
    """
    Отправка email Администратору при создании уникального вопроса.
    """
    admin_email = User.objects.get(username="admin").email
    send_mail(
        "Поступил новый вопрос",
        question,
        from_email=admin_email,
        recipient_list=[
            admin_email,
        ],
        fail_silently=False,
    )

