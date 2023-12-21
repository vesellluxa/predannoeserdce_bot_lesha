from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from users.models import TelegramUser
from questions.models import UniqueQuestion, FrequentlyAskedQuestion
from constants import (USERNAME_REGEX, USERNAME_MIN_LENGTH,
                       USERNAME_MAX_LENGTH, NAME_REGEX,
                       PHONE_NUMBER, FAQ_MAX_LENGTH, NAME_MIN_LENGTH,
                       NAME_MAX_LENGTH, CHAT_ID_LENGTH)


class UserCreateSerializer(ModelSerializer):
    """Сериализатор для создания первой записи пользователя."""
    username = serializers.RegexField(
        regex=USERNAME_REGEX,
        min_length=USERNAME_MIN_LENGTH,
        max_length=USERNAME_MAX_LENGTH,
        validators=[
            UniqueValidator(queryset=TelegramUser.objects.all())
        ]
    )

    class Meta:
        model = TelegramUser
        fields = ('username', )


class UserSerializer(ModelSerializer):
    """Сериализатор для добавления данных пользователя."""
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
        fields = ('name', 'surname', 'email', 'phone', 'chat_id',)


class FrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка вопросов."""
    class Meta:
        model = FrequentlyAskedQuestion
        fields = ('text', 'id',)


class FaqAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа на выбранный вопрос."""
    class Meta:
        model = FrequentlyAskedQuestion
        fields = ('answer',)


class UniqueQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для уникального вопроса пользователя."""
    text = serializers.CharField(max_length=FAQ_MAX_LENGTH,)
    owner = TelegramUser

    class Meta:
        model = UniqueQuestion
        fields = ('text', 'owner',)
        extra_kwargs = {'text': {'required': True}}


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""
    pass
