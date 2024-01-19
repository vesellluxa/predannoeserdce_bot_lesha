from django.db import models

from users.models import TelegramUser, TimeMixin


class BaseNotification(models.Model, TimeMixin):
    """
    Абстрактная модель для уведомлений.
    """

    text = models.CharField(
        verbose_name="Текст уведомления",
        max_length=1024
    )
    is_finished = models.BooleanField(
        verbose_name="Завершена ли рассылка?",
        default=False
    )

    def __str__(self):
        return self.text

    class Meta:
        abstract = True


class Notification(BaseNotification):
    """
    Модель для уведомлений.
    """

    to = models.ForeignKey(
        verbose_name="Пользователь, получающий уведомление",
        to=TelegramUser,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Уведомлениие для пользователей Telegram"


class TelegramNewsletter(BaseNotification):
    """
    Модель для рассылки.
    """

    sending_date = models.DateTimeField(
        verbose_name="Дата отправки"
    )

    class Meta:
        """
        Сортировка по дате рассылки.
        """

        ordering = ("-sending_date",)

        verbose_name = "Рассылка для пользователей Telegram"
        verbose_name_plural = "Рассылки для пользователей Telegram"

    def __str__(self):
        return self.text
