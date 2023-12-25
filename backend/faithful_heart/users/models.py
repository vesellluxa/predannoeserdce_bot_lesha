from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from faithful_heart import constants


class User(AbstractUser):
    """Модель для менеджера приюта."""

    chat_id = models.CharField(
        verbose_name='Чат ID',
        max_length=constants.CHAT_ID_LENGTH
    )


class TelegramUser(models.Model):
    """Модель для сбора данных пользователей."""

    username = models.CharField(
        max_length=constants.USERNAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(
                constants.USERNAME_MIN_LENGTH)],
        verbose_name='Имя пользователя',
        unique=True
    )
    email = models.EmailField(
        verbose_name='E-mail пользователя',
        unique=True
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=constants.NAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(
                constants.NAME_MIN_LENGTH)]
    )
    surname = models.CharField(
        verbose_name='Фамилия',
        max_length=constants.SURNAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(
                constants.SURNAME_MIN_LENGHT)]
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=constants.PHONE_LENGTH,
        validators=[RegexValidator(constants.PHONE_NUMBER)],
        unique=True
    )

    chat_id = models.CharField(
        max_length=constants.CHAT_ID_LENGTH,
        unique=True
    )

    class Meta:
        """Сортировка по имени."""

        ordering = ('name',)
