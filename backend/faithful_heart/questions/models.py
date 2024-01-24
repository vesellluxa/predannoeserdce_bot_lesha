from django.db import models

from questions.utils import (create_notification_to_user,
                             create_telegram_notification_to_admin,
                             send_email_to_admin)
from users.models import TelegramUser, TimeMixin
from faithful_heart import constants


class AbstractQuestion(models.Model, TimeMixin):
    """
    Абстрактная модель вопроса.
    """

    text = models.TextField(max_length=constants.FAQ_MAX_LENGTH,
                            verbose_name='Текст вопроса', )

    def __str__(self):
        return self.text

    class Meta:
        abstract = True


class FrequentlyAskedQuestion(AbstractQuestion):
    """
    Модель FAQ (Часто задаваемые вопросы).
    """

    class QuestionCategories(models.TextChoices):
        FAQ = constants.FAQ
        SHELTER_INFO = constants.SHELTER_INFO
        NEEDS = constants.NEEDS
        DONATIONS = constants.DONATIONS
        LIST_ANIMALS = constants.LIST_ANIMALS

    answer = models.TextField(
        max_length=constants.FAQ_MAX_LENGTH,
        verbose_name='Текст ответа'
    )

    is_relevant = models.BooleanField(
        verbose_name="Актуален ли вопрос?",
        default=True
    )

    category = models.CharField(
        verbose_name="Категория вопроса",
        max_length=constants.CATEGORY_MAX_LENGTH,
        choices=QuestionCategories.choices,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = "FAQ (Часто задаваемые вопросы)"
        verbose_name_plural = "FAQ (Часто задаваемые вопросы)"


class UniqueQuestion(AbstractQuestion, TimeMixin):
    """
    Модель уникального вопроса от пользователя.
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

    def __str__(self):
        return self.text

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
