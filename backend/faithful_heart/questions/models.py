from django.conf import settings
from django.db import models
from users.models import TelegramUser
from faithful_heart import constants
from questions.validators import validate_is_profane_russian


class AbstractQuestion(models.Model):
    """Абстрактная модель FAQ."""

    text = models.TextField(max_length=constants.FAQ_MAX_LENGTH,
                            verbose_name='Текст вопроса',
                            validators=[validate_is_profane_russian])

    class Meta:
        """Абстрактная модель."""

        abstract = True


class FrequentlyAskedQuestion(AbstractQuestion):
    """Модель FAQ."""

    answer = models.TextField(max_length=constants.FAQ_MAX_LENGTH,
                              verbose_name='Текст ответа')
    is_main = models.BooleanField()
    is_relevant = models.BooleanField()


class UniqueQuestion(AbstractQuestion):
    """Модель для уникального вопроса."""

    owner = models.ForeignKey(TelegramUser,
                              on_delete=models.CASCADE,
                              verbose_name='Автор вопроса')
    answer = models.TextField(max_length=constants.FAQ_MAX_LENGTH,
                              verbose_name='Текст ответа',
                              blank=True)

    @property
    def is_answered(self):
        """Функция, определяющая был ли получени ответ на вопрос."""
        return self.answer != ''
