from django.db import models
from users.models import TelegramUser, TimeMixin
from faithful_heart import constants


class BaseNotification(models.Model, TimeMixin):
    text = models.CharField(
        verbose_name="Текст уведомления",
        max_length=1024
    )
    is_finished = models.BooleanField(
        verbose_name="Завершена ли рассылка",
        default=False
    )

    class Meta:
        abstract = True


class Notification(BaseNotification):
    to = models.ForeignKey(
        verbose_name="Пользователь, получающий уведомление",
        to=TelegramUser,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Уведомлениие для пользователей Telegram"


class TelegramNewsletter(BaseNotification):
    sending_date = models.DateTimeField(
        verbose_name="Дата отправки"
    )

    class Meta:
        verbose_name = "Рассылка для пользователей Telegram"
        verbose_name_plural = "Рассылки для пользователей Telegram"
