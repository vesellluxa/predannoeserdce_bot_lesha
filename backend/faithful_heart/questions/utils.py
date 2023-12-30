from django.core.mail import send_mail

from faithful_heart import constants
from faithful_heart.settings import EMAIL_HOST_USER
from notifications.models import Notification

from users.models import User, TelegramUser


def create_telegram_notification_to_admin(question):
    url_to_question = (constants.PROD_URL +
                       f"/admin/questions/uniquequestion/{question.pk}/change/")
    Notification.objects.create(
        to=TelegramUser.get_admin_telegram_user(),
        text=f"Поступил новый вопрос. Ссылка: {url_to_question}"
    )


def create_notification_to_user(question):
    Notification.objects.create(
        to=question.owner,
        text=f"Поступил ответ на ваш вопрос:"
             f"{question.answer}"
    )


def send_email_to_admin(question):
    """
    Отправка email Администратору при создании уникального вопроса.
    """
    url_to_question = (constants.PROD_URL +
                       f"/admin/questions/uniquequestion/{question.pk}/change/")
    text = f"Поступил новый вопрос. Ссылка: {url_to_question}"
    send_mail(
        subject="Поступил новый вопрос",
        message=text,
        from_email=EMAIL_HOST_USER,
        recipient_list=[
            User.objects.get(username="admin").email,
        ],
        fail_silently=False,
    )

