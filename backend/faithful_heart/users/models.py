from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class Manager(AbstractUser):
    """Модель для менеджера приюта."""

    chat_id = models.IntegerField()


class TelegramUser(models.Model):
    """Модель для сбора данных пользователей."""

    username = models.CharField(min_lenght=settings.USERNAME_MIN_LENGTH,
                                max_length=settings.USERNAME_MAX_LENGTH,
                                verbose_name='Имя пользователя')
    email = models.EmailField(verbose_name='E-mail пользователя')
    name = models.CharField(verbose_name='Имя')
    phone = models.CharField(validators=[RegexValidator(settings.PHONE_NUMBER)])
    chat_id = models.IntegerField()

    class Meta:
        ordering = ('name',)
