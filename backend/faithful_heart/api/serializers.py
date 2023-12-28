from rest_framework import serializers

from users.models import TelegramUser
from questions.models import UniqueQuestion, FrequentlyAskedQuestion
from questions.validators import validate_is_profane_russian


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
            "second_name",
            "surname",
            "email",
            "phone_number",
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
