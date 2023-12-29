from django.db import models
from users.models import TelegramUser, TimeMixin
from faithful_heart import constants


class AbstractQuestion(models.Model, TimeMixin):
    """
    Абстрактная модель Вопроса.
    """

    text = models.TextField(max_length=constants.FAQ_MAX_LENGTH,
                            verbose_name='Текст вопроса',)

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

    answer = models.TextField(
        max_length=constants.FAQ_MAX_LENGTH,
        verbose_name='Текст ответа'
    )
    is_relevant = models.BooleanField()
    category = models.CharField(
        max_length=24,
        choices=QuestionCategories.choices,
        null=False,
        blank=False
    )


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

    @property
    def is_answered(self):
        """
        Функция, определяющая был ли получени ответ на вопрос.
        """
        return self.answer != ''
