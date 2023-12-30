from django.db import models

from questions.utils import (create_notification_to_user,
                             create_telegram_notification_to_admin,
                             send_email_to_admin)
from users.models import TelegramUser, TimeMixin
from faithful_heart import constants


class AbstractQuestion(models.Model, TimeMixin):
    """
    Абстрактная модель Вопроса.
    """

    text = models.TextField(max_length=constants.FAQ_MAX_LENGTH,
                            verbose_name='Текст вопроса', )

    class Meta:
        abstract = True


class FrequentlyAskedQuestion(AbstractQuestion):
    """
    Модель FAQ (Часто задаваемые вопросы).
    """

    class QuestionCategories(models.TextChoices):
        FAQ = "FAQ", "Часто Задаваемые Вопросы"
        SHELTER_INFO = "Shelter_Info", "Узнать больше о приюте"
        NEEDS = "Needs", "Нужды приюта"
        DONATIONS = "Donations", "Сделать пожертвование"
        LIST_ANIMALS = "List_Animals", "Список животных"

    answer = models.TextField(
        max_length=constants.FAQ_MAX_LENGTH,
        verbose_name='Текст ответа'
    )

    is_relevant = models.BooleanField(
        verbose_name="Актуален ли вопрос?",
        default=True
    )

    category = models.CharField(
        max_length=24,
        choices=QuestionCategories.choices,
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class UniqueQuestion(AbstractQuestion, TimeMixin):
    """
    Модель уникального вопроса.
    """

    owner = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        verbose_name='Автор вопроса'
    )

    answer = models.TextField(
        max_length=constants.FAQ_MAX_LENGTH,
        verbose_name='Текст ответа',
        blank=True
    )

    class Meta:
        verbose_name = "Вопрос от пользователя"
        verbose_name_plural = "Вопросы от пользователей"

    @property
    def is_answered(self):
        """
        Функция, определяющая был ли получени ответ на вопрос.
        """
        return self.answer != ''

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.is_answered:
            create_telegram_notification_to_admin(self)
            send_email_to_admin(self)
        if self.is_answered:
            create_notification_to_user(self)
