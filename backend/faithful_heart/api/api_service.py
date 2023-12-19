import csv
import datetime as dt

from django.core.mail import send_mail
from rest_framework.response import Response
from openpyxl import Workbook
from aiogram import Bot

from constants import DATETIME_FORMAT, ADMIN_EMAIL, ADMIN_TG_CHAT_ID


def export_users_excel(users):
    """Создание файла excel с данными пользователей."""
    date_now = dt.datetime.now()
    date_now_formatted = date_now.strftime(DATETIME_FORMAT)
    response = Response(content_type='application/ms-excel; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=f"Пользователи_{date_now_formatted}.xls"'
    workbook = Workbook()
    sheet = workbook.active
    headers = ['Name', 'Phone', 'Username', 'Chat_id', 'Email']
    sheet.append(headers)
    for user in users:
        sheet.append([user.name, user.phone, user.username,
                            user.chat_id, user.email])
    workbook.save(response)

    return response


def send_email_to_admin(question):
    """Письмо админу при появлении уникального вопроса."""
    send_mail('Поступил новый вопрос', question, [ADMIN_EMAIL], fail_silently=False)


async def send_tg_notification_to_admin(question):
    """Уведомление админу в Telegram
    при появлении уникального вопроса."""
    bot = Bot(token=constants.TOKEN)
    await bot.send_message(chat_id=ADMIN_TG_CHAT_ID,
        text=f'Поступил новый вопрос: {question}')
