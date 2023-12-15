import csv
import datetime as dt

from django.core.mail import send_mail
from rest_framework.response import Response
from aiogram import Bot, types


def create_excel_file(users):
    response = Response(
            users,
            content_type='application/vnd.ms-excel; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Пользователи.xls"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone', 'Username', 'Chat_id', 'Email'])
    for user in users:
        writer.writerow([user.name, user.phone, user.username,
                            user.chat_id, user.email])

    return response


def send_email_to_admin(question):
    send_mail(f'Поступил новый вопрос', question, (ADMIN_EMAIL, ), fail_silently=False)


def send_tg_notification_to_admin(question):
    bot = Bot(token=TOKEN)
    bot.send_message(chat_id=ADMIN_TG_CHAT_ID,
    text=f'Поступил новый вопрос: {question}')
