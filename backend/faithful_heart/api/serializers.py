from rest_framework import serializers

from notifications.models import Notification, TelegramNewsletter
from questions.models import FrequentlyAskedQuestion, UniqueQuestion
from questions.validators import validate_is_profane_russian
from users.models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя.
    """

    class Meta:
        model = TelegramUser
        fields = (
            "username",
            "chat_id",
            "name",
            "surname",
            "middle_name",
            "surname",
            "email",
            "phone_number",
            "consent_to_save_personal_data",
        )


class TelegramUserShortSerializer(TelegramUserSerializer):
    class Meta:
        model = TelegramUser
        fields = (
            "chat_id",
        )


class FrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа на выбранный вопрос."""

    class Meta:
        model = FrequentlyAskedQuestion
        fields = (
            "text",
            "answer",
            "id",
        )


class UniqueQuestionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для уникального вопроса от пользователя.
    """

    owner = serializers.SlugRelatedField(
        queryset=TelegramUser.objects.all(), slug_field="chat_id"
    )

    def validate_text(self, text):
        validate_is_profane_russian(text)
        return text

    class Meta:
        model = UniqueQuestion
        fields = (
            "text",
            "owner",
        )


class NotificationSerializer(serializers.ModelSerializer):
    to = TelegramUserShortSerializer()

    class Meta:
        model = Notification
        fields = (
            "id",
            "text",
            "to",
            "is_finished"
        )


class NewsletterSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = TelegramNewsletter
        fields = (
            "id",
            "text",
            "sending_date",
            "is_finished",
            "users"
        )

    def get_users(self, value):
        return list(TelegramUser.objects.values_list('chat_id', flat=True))
