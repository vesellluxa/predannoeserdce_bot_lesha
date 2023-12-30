from django.db import models
from users.models import TelegramUser, TimeMixin
from notifications.models import Notification
from faithful_heart import constants


class AbstractQuestion(models.Model, TimeMixin):
    """
    Абстрактная модель Вопроса.
    """

    text = models.TextField(max_length=constants.FAQ_MAX_LENGTH,
                            verbose_name='Текст вопроса', )

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
        DONATIONS = "Donations", "Сделать пожертвование"

    answer = models.TextField(
        max_length=constants.FAQ_MAX_LENGTH,
        verbose_name='Текст ответа'
    )

    is_relevant = models.BooleanField(default=True)

    category = models.CharField(
        max_length=24,
        choices=QuestionCategories.choices,
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


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

    class Meta:
        verbose_name = "Вопрос от пользователя"
        verbose_name_plural = "Вопросы от пользователей"

    @property
    def is_answered(self):
        """
        Функция, определяющая был ли получени ответ на вопрос.
        """
        return self.answer != ''

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.is_answered:
            url_to_question = constants.PROD_URL + f"/admin/questions/uniquequestion/{self.pk}/change/"
            print(url_to_question)
            Notification.objects.create(
                to=TelegramUser.get_admin_telegram_user(),
                text=f"Поступил новый вопрос. Ссылка: {url_to_question}"
            )
        if self.is_answered:
            Notification.objects.create(
                to=self.owner,
                text=f"Поступил ответ на ваш вопрос:"
                     f"{self.answer}"

            )
