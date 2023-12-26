from rest_framework import serializers

from users.models import TelegramUser
from questions.models import UniqueQuestion, FrequentlyAskedQuestion
from faithful_heart import constants
from questions.validators import validate_is_profane_russian


class TelegramUserSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка вопросов."""

    class Meta:
        model = FrequentlyAskedQuestion
        fields = ('text', 'answer', 'id', )


class FrequentlyAskedQuestionAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа на выбранный вопрос."""

    class Meta:
        model = TelegramUser
        fields = ('username', 'chat_id', 'name', 'surname', 'email', 'phone',)


class UniqueQuestionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для уникального вопроса от пользователя.
    """
    owner = serializers.SlugRelatedField(
        queryset=TelegramUser.objects.all(),
        slug_field='chat_id'
    )

    def validate_text(self, text):
        validate_is_profane_russian(text)
        return text

    class Meta:
        model = UniqueQuestion
        fields = ('text', 'owner',)
