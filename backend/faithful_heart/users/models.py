from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models


class User(AbstractUser):
    """Модель для менеджера приюта."""

    chat_id = models.IntegerField()


class TelegramUser(models.Model):
    """Модель для сбора данных пользователей."""

    username = models.CharField(max_length=settings.USERNAME_MAX_LENGTH,
                                validators=[
                                    MinLengthValidator(
                                        settings.USERNAME_MIN_LENGHT)],
                                verbose_name='Имя пользователя')
    email = models.EmailField(verbose_name='E-mail пользователя')
    name = models.CharField(verbose_name='Имя',
                            max_length=settings.NAME_LENGTH)
    phone = models.CharField(max_length=settings.PHONE_LENGTH,
                             validators=[RegexValidator(settings.PHONE_NUMBER)]
                             )

    chat_id = models.CharField(max_length=settings.CHAT_ID_LENGTH)

    class Meta:
        """Сортировка по имени."""

        ordering = ('name',)
