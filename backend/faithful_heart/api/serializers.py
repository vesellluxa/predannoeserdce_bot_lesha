from rest_framework import serializers

from users.models import TelegramUser
from questions.models import UniqueQuestion, FrequentlyAskedQuestion
from faithful_heart import constants


class TelegramUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и изменения данных пользователя.
    """

    class Meta:
        model = TelegramUser
        fields = ('username', 'chat_id', 'name', 'surname', 'email', 'phone',)


class FrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    """
    Сериализатор часто задаваемых вопросов.
    """

    class Meta:
        model = FrequentlyAskedQuestion
        fields = ('text', 'answer', 'id',)


class UniqueQuestionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для уникального вопроса от пользователя.
    """
    owner = serializers.SlugRelatedField(
        queryset=TelegramUser.objects.all(),
        slug_field='chat_id'
    )

    class Meta:
        model = UniqueQuestion
        fields = ('text', 'owner',)
