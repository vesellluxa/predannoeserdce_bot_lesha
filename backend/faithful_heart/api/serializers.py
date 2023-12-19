from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from users.models import TelegramUser
from questions.models import UniqueQuestion, FrequentlyAskedQuestion
from constants import (USERNAME_REGEX, USERNAME_MIN_LENGTH,
                       USERNAME_MAX_LENGTH, NAME_REGEX,
                       PHONE_NUMBER, FAQ_MAX_LENGTH, NAME_MIN_LENGTH,
                       NAME_MAX_LENGTH, CHAT_ID_LENGTH)


class UserSerializer(ModelSerializer):
    """Сериализатор пользователя."""
    username = serializers.RegexField(
        regex=USERNAME_REGEX,
        min_length=USERNAME_MIN_LENGTH,
        max_length=USERNAME_MAX_LENGTH,
        validators=[
            UniqueValidator(queryset=TelegramUser.objects.all())
        ]
    )
    name = serializers.RegexField(
        regex=NAME_REGEX,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH
    )
    surname = serializers.RegexField(
        regex=NAME_REGEX,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=TelegramUser.objects.all())
        ]
    )
    phone = serializers.RegexField(regex=PHONE_NUMBER,)
    chat_id = serializers.RegexField(
        regex=PHONE_NUMBER,
        max_length=CHAT_ID_LENGTH)


    class Meta:
        model = TelegramUser
        fields = ('username')


class FrequentlyAskedQuestionSerializer(ModelSerializer):
    """Сериализатор для получения списка вопросов."""
    class Meta:
        model = FrequentlyAskedQuestion
        fields = ('text', 'id')


class FaqAnswerSerializer(ModelSerializer):
    """Сериализатор для ответа на выбранный вопрос."""
    class Meta:
        model = FrequentlyAskedQuestion
        fields = ('answer',)


class UniqueQuestionSerializer(ModelSerializer):
    """Сериализатор для уникального вопроса пользователя."""
    text = serializers.CharField(max_length=FAQ_MAX_LENGTH,)

    class Meta:
        model = UniqueQuestion
        fields = ('text',)
        extra_kwargs = {'text': {'required': True}}


class TokenSerializer(Serializer):
    """Сериализатор токена."""
    pass
