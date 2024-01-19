from django.core.mail import send_mail

from notifications.models import Notification
from users.models import TelegramUser, User
from faithful_heart import constants
from faithful_heart.settings import EMAIL_HOST_USER


def create_telegram_notification_to_admin(question) -> None:
    """
    Создание уведомления администратору
    о поступлении нового вопроса от пользователя.
    """
    question_url = f"/admin/questions/uniquequestion/{question.pk}/change/"
    full_url = constants.PROD_URL + question_url
    Notification.objects.create(
        to=TelegramUser.get_admin_telegram_user(),
        text=f"Поступил новый вопрос. Ссылка: {full_url}"
    )


def create_notification_to_user(question) -> None:
    """
    Создание уведомления пользователю
    об ответе на его вопрос.
    """
    Notification.objects.create(
        to=question.owner,
        text=f"Поступил ответ на ваш вопрос {question.text}:"
             f"{question.answer}"
    )


def send_email_to_admin(question) -> None:
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
