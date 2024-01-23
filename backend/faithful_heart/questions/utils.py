from django.core.mail import send_mail

from notifications.models import Notification
from users.models import TelegramUser, User
from faithful_heart import constants
from faithful_heart.settings import EMAIL_HOST_USER


def create_telegram_notification_to_admin(question):
    question_url = f"/admin/questions/uniquequestion/{question.pk}/change/"
    full_url = constants.PROD_URL + question_url
    Notification.objects.bulk_create([
        Notification(
            to=user,
            text=f"Поступил новый вопрос. Ссылка: {full_url}"
        ) for user in TelegramUser.objects.filter(
            username__in=User.objects.filter(
                telegram_username__isnull=False
            ).values_list("telegram_username", flat=True)
        )
    ])


def create_notification_to_all_user(message: str):
    Notification.objects.bulk_create([
        Notification(
            to=user,
            text=message
        ) for user in User.objects.filter(
            email__isnull=False
        )
    ])


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
    question_url = f"/admin/questions/uniquequestion/{question.pk}/change/"
    full_url = constants.PROD_URL + question_url
    text = f"Поступил новый вопрос. Ссылка: {full_url}"
    send_mail(
        subject="Поступил новый вопрос",
        message=text,
        from_email=EMAIL_HOST_USER,
        recipient_list=[
            User.objects.get(username="admin").email,
        ],
        fail_silently=False,
    )
