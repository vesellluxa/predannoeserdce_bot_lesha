from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from faithful_heart import constants


class TimeMixin:
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    """Модель для менеджера приюта."""

    chat_id = models.CharField(
        verbose_name='Чат ID',
        max_length=constants.CHAT_ID_LENGTH
    )


class TelegramUser(models.Model, TimeMixin):
    """
    Модель для сбора данных пользователей.
    """

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
        unique=True,
        blank=True,
        null=True

    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=constants.NAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(
                constants.NAME_MIN_LENGTH)],
        blank=True
    )
    second_name = models.CharField(
        verbose_name='Фамилия',
        max_length=constants.SURNAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(
                constants.SURNAME_MIN_LENGHT)],
        blank=True
    )
    surname = models.CharField(
        verbose_name='Отчество',
        max_length=constants.SURNAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(
                constants.SURNAME_MIN_LENGHT)],
        blank=True
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=constants.PHONE_LENGTH,
        validators=[RegexValidator(constants.PHONE_NUMBER)],
        unique=True,
        blank=True,
        null=True
    )

    chat_id = models.CharField(
        max_length=constants.CHAT_ID_LENGTH,
        unique=True
    )

    class Meta:
        """
        Сортировка по имени.
        """

        ordering = ('name',)

    @property
    def is_fully_filled(self):
        """
        Проверяет заполнены ли дополнительные поля пользователя.
        """
        fields_list = [
            self.name, self.second_name, self.surname, self.phone_number, self.email
        ]
        if any(field is None or field == '' for field in fields_list) is True:
            return False
        return True
