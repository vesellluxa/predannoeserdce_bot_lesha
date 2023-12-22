from rest_framework import serializers

from users.models import TelegramUser
from questions.models import UniqueQuestion, FrequentlyAskedQuestion


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания первой записи пользователя."""

    class Meta:
        model = TelegramUser
        fields = ('username', 'chat_id', )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления данных пользователя."""

    class Meta:
        model = TelegramUser
        fields = ('name', 'surname', 'email', 'phone', )


class FrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка вопросов."""
    class Meta:
        model = FrequentlyAskedQuestion
        fields = ('text', 'id', )


class FrequentlyAskedQuestionAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа на выбранный вопрос."""
    class Meta:
        model = FrequentlyAskedQuestion
        fields = ('answer', )


class UniqueQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для уникального вопроса пользователя."""
    owner = serializers.SlugRelatedField(
        queryset=TelegramUser.objects.all(),
        many=False,
        slug_field='chat_id',
    )

    class Meta:
        model = UniqueQuestion
        fields = ('text', 'owner', )
        lookup_field = 'chat_id'


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""
    pass
