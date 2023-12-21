from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from constants import (CHAT_ID_LENGTH, USERNAME_MIN_LENGTH, NAME_MAX_LENGTH,
                       CHAT_ID_LENGTH, USERNAME_MAX_LENGTH, NAME_MIN_LENGTH,
                       SURNAME_MAX_LENGTH, SURNAME_MIN_LENGHT, PHONE_LENGTH,
                       PHONE_NUMBER)


class User(AbstractUser):
    """Модель для менеджера приюта."""

    chat_id = models.CharField(verbose_name='Чат ID',
                               max_length=CHAT_ID_LENGTH)


class TelegramUser(models.Model):
    """Модель для сбора данных пользователей."""

    username = models.CharField(max_length=USERNAME_MAX_LENGTH,
                                validators=[
                                    MinLengthValidator(
                                        USERNAME_MIN_LENGTH)],
                                verbose_name='Имя пользователя')
    email = models.EmailField(verbose_name='E-mail пользователя')
    name = models.CharField(verbose_name='Имя',
                            max_length=NAME_MAX_LENGTH,
                            validators=[
                                MinLengthValidator(
                                    NAME_MIN_LENGTH)])
    surname = models.CharField(verbose_name='Фамилия',
                               max_length=SURNAME_MAX_LENGTH,
                               validators=[
                                   MinLengthValidator(
                                       SURNAME_MIN_LENGHT)])
    phone = models.CharField(verbose_name='Номер телефона',
                             max_length=PHONE_LENGTH,
                             validators=[RegexValidator(PHONE_NUMBER)]
                             )

    chat_id = models.CharField(max_length=CHAT_ID_LENGTH)

    class Meta:
        """Сортировка по имени."""

        ordering = ('name',)
