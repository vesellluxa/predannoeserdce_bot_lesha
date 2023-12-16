from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models


class User(AbstractUser):
    """Модель для менеджера приюта."""

    chat_id = models.CharField(verbose_name='Чат ID',
                               max_length=settings.CHAT_ID_LENGTH)


class TelegramUser(models.Model):
    """Модель для сбора данных пользователей."""

    username = models.CharField(max_length=settings.USERNAME_MAX_LENGTH,
                                validators=[
                                    MinLengthValidator(
                                        settings.USERNAME_MIN_LENGHT)],
                                verbose_name='Имя пользователя')
    email = models.EmailField(verbose_name='E-mail пользователя')
    name = models.CharField(verbose_name='Имя',
                            max_length=settings.NAME_MAX_LENGTH,
                            validators=[
                                MinLengthValidator(
                                    settings.NAME_MIN_LENGHT)])
    surname = models.CharField(verbose_name='Имя',
                               max_length=settings.SURNAME_MAX_LENGTH,
                               validators=[
                                   MinLengthValidator(
                                       settings.SURNAME_MIN_LENGHT)])
    phone = models.CharField(max_length=settings.PHONE_LENGTH,
                             validators=[RegexValidator(settings.PHONE_NUMBER)]
                             )

    chat_id = models.CharField(max_length=settings.CHAT_ID_LENGTH)

    class Meta:
        """Сортировка по имени."""

        ordering = ('name',)
