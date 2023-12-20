from datetime import datetime

from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.core.mail import send_mail
from rest_framework.response import Response
from openpyxl import Workbook
from aiogram import Bot

from constants import DATETIME_FORMAT, ADMIN_EMAIL, ADMIN_TG_CHAT_ID, TOKEN
from faithful_heart.settings import MEDIA_ROOT


def export_users_excel(users):
    """Создание файла excel с данными пользователей."""
    date_now = datetime.now()
    date_now_formatted = date_now.strftime(DATETIME_FORMAT)
    workbook = Workbook()
    sheet = workbook.active
    headers = ['Name', 'Surname', 'Phone', 'Username', 'Chat_id', 'Email']
    sheet.append(headers)
    for user in users:
        sheet.append([user.name, user.surname, user.phone, user.username,
                            user.chat_id, user.email])
    workbook.save(f'{MEDIA_ROOT}/Пользователи_'+date_now_formatted+'.xlsx')


def send_email_to_admin(question):
    """Письмо админу при появлении уникального вопроса."""
    send_mail('Поступил новый вопрос', question, from_email=ADMIN_EMAIL,
                recipient_list=[ADMIN_EMAIL,], fail_silently=False)

@async_to_sync
async def send_tg_notification_to_admin(question):
    """Уведомление админу в Telegram
    при появлении уникального вопроса."""
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=ADMIN_TG_CHAT_ID,
        text=f'Поступил новый вопрос: {question}')
