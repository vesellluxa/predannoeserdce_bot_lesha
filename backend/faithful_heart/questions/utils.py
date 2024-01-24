from django.core.mail import send_mail

from notifications.models import Notification
from users.models import TelegramUser, User
from faithful_heart import constants
from faithful_heart.settings import EMAIL_HOST_USER


def create_telegram_notification_to_admin(question):
    Notification.objects.bulk_create([
        Notification(
            to=user,
            text=constants.ADMIN_NOTIFICATION.format(
                constants.URL_TO_QUESTION.format(question.pk)
            )
        ) for user in TelegramUser.objects.filter(
            username__in=User.objects.filter(
                telegram_username__isnull=False
            ).values_list(
                "telegram_username",
                flat=True
            )
        )
    ])


def create_notification_to_user(question) -> None:
    """
    Создание уведомления пользователю
    об ответе на его вопрос.
    """
    Notification.objects.create(
        to=question.owner,
        text=constants.USER_NOTIFICATION.format(question.text, question.answer)
    )


def send_email_to_admin(question) -> None:
    """
    Отправка email Администратору при создании уникального вопроса.
    """
    send_mail(
        subject="Поступил новый вопрос",
        message=constants.ADMIN_NOTIFICATION.format(
            constants.URL_TO_QUESTION.format(question.pk)
        ),
        from_email=EMAIL_HOST_USER,
        recipient_list=[
            user.email for user in User.objects.filter(email__isnull=False)
        ],
        fail_silently=False,
    )
