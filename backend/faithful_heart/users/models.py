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

    telegram_username = models.CharField(
        max_length=constants.USERNAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(constants.USERNAME_MIN_LENGTH),
            RegexValidator(
                regex=constants.TELEGRAM_USERNAME_REGEX,
                message=constants.USERNAME_REGEX_VALIDATOR_ERROR_TEXT,
                code="invalid_username"
            )
        ],
        verbose_name="Имя пользователя в telegram",
        unique=True,
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь админ-панели"
        verbose_name_plural = "Пользователи админ-панели"

    def save(self, *args, **kwargs):
        self.telegram_username = self.telegram_username.lower()
        super().save(*args, **kwargs)


class TelegramUser(models.Model, TimeMixin):
    """
    Модель для сбора данных пользователей.
    """

    username = models.CharField(
        max_length=constants.USERNAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(constants.USERNAME_MIN_LENGTH),
            RegexValidator(
                regex=constants.TELEGRAM_USERNAME_REGEX,
                message=constants.USERNAME_REGEX_VALIDATOR_ERROR_TEXT,
                code="invalid_username"
            )
        ],
        verbose_name="Имя пользователя",
        unique=True,
    )

    email = models.EmailField(
        verbose_name="E-mail пользователя", unique=True, blank=True, null=True
    )

    name = models.CharField(
        verbose_name="Имя",
        max_length=constants.NAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(constants.NAME_MIN_LENGTH),
            RegexValidator(
                regex=constants.NAME_REGEX,
                message=constants.NAME_REGEX_VALIDATOR_ERROR_TEXT,
                code="invalid_name"
            )
        ],
        blank=True,
    )

    surname = models.CharField(
        verbose_name="Фамилия",
        max_length=constants.SURNAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(constants.NAME_MIN_LENGTH),
            RegexValidator(
                regex=constants.NAME_REGEX,
                message=constants.SURNAME_REGEX_VALIDATOR_ERROR_TEXT,
                code="invalid_second_name"
            )
        ],
        blank=True,
    )

    middle_name = models.CharField(
        verbose_name="Отчество",
        max_length=constants.SURNAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(constants.NAME_MIN_LENGTH),
            RegexValidator(
                regex=constants.NAME_REGEX,
                message=constants.PATRONYMIC_REGEX_VALIDATOR_ERROR_TEXT,
                code="invalid_surname"
            )
        ],
        blank=True,
    )

    phone_number = models.CharField(
        verbose_name="Номер телефона",
        max_length=constants.PHONE_NUMBER_LENGTH,
        validators=[
            RegexValidator(
                regex=constants.PHONE_NUMBER_REGEX,
                message=constants.PHONE_NUMBER_REGEX_VALIDATOR_ERROR_TEXT,
                code='invalid_phone_number'
            )
        ],
        unique=True,
        blank=True,
        null=True,
    )

    chat_id = models.CharField(
        max_length=constants.CHAT_ID_MAX_LENGTH,
        unique=True,
        validators=[
            MinLengthValidator(constants.CHAT_ID_MIN_LENGTH),
            RegexValidator(
                regex=constants.CHAT_ID_REGEX,
                message=constants.CHAT_ID_REGEX_VALIDATOR_ERROR_TEXT,
                code='invalid_chat_id'
            )
        ]
    )

    class Meta:
        """
        Сортировка по имени.
        """

        ordering = ("name",)

        verbose_name = "Telegram пользователь"
        verbose_name_plural = "Telegram пользователи"

    def __str__(self):
        return self.username

    @property
    def is_fully_filled(self):
        """
        Проверяет заполнены ли дополнительные поля пользователя.
        """
        fields_list = [
            self.name,
            self.phone_number,
            self.email,
        ]
        if any(field is None or field == "" for field in fields_list) is True:
            return False
        return True

    @staticmethod
    def get_admin_telegram_user():
        return TelegramUser.objects.filter(
            username=User.objects.get(username="admin").telegram_username
        ).first()
