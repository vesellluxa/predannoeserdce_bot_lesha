from datetime import datetime
from dotenv import load_dotenv
import os

from asgiref.sync import async_to_sync
from django.core.mail import send_mail
from openpyxl import Workbook
from aiogram import Bot

from faithful_heart import constants
from faithful_heart.settings import MEDIA_ROOT


load_dotenv()

TOKEN = os.getenv('TOKEN')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_TG_CHAT_ID = os.getenv('ADMIN_TG_CHAT_ID')


def export_users_excel(users):
    """Создание файла excel с данными пользователей."""
    date_now = datetime.now()
    date_now_formatted = date_now.strftime(constants.DATETIME_FORMAT)
    workbook = Workbook()
    sheet = workbook.active
    sheet.column_dimensions['A'].width = 10
    sheet.column_dimensions['B'].width = 15
    sheet.column_dimensions['C'].width = 18
    sheet.column_dimensions['D'].width = 18
    sheet.column_dimensions['E'].width = 18
    sheet.column_dimensions['F'].width = 18
    headers = ['Name', 'Surname', 'Phone', 'Username', 'Chat_id', 'Email']
    sheet.append(headers)
    for user in users:
        sheet.append([user.name, user.surname, user.phone, user.username,
                            user.chat_id, user.email])
    workbook.save(f'{MEDIA_ROOT}/Пользователи_{date_now_formatted}.xlsx')


def send_email_to_admin(question):
    """Письмо админу при появлении уникального вопроса."""
    send_mail('Поступил новый вопрос', question, from_email=ADMIN_EMAIL,
                recipient_list=[ADMIN_EMAIL, ], fail_silently=False)


@async_to_sync
async def send_tg_notification_to_admin(question):
    """Уведомление админу в Telegram
    при появлении уникального вопроса."""
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=ADMIN_TG_CHAT_ID,
        text=f'Поступил новый вопрос: {question}')
