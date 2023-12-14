from django.conf import settings
from django.db import models
from users.models import TelegramUser


class FrequentlyAskedQuestion(models.Model):
    """Модель FAQ."""

    text = models.TextField(max_length=settings.FAQ_MAX_LENGTH,
                            verbose_name='Текст вопроса')
    answer = models.TextField(max_length=settings.FAQ_MAX_LENGTH,
                              verbose_name='Текст ответа',
                              blank=True)
    is_relevant = models.BooleanField()
    is_main = models.BooleanField()


class UniqueQuestion(FrequentlyAskedQuestion):
    """Модель для уникального вопроса."""

    owner = models.ForeignKey(TelegramUser,
                              on_delete=models.CASCADE,
                              verbose_name='Автор вопроса')

    @property
    def is_answered(self):
        self.answer != ''
