from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import TelegramUser
from questions.models import UniqueQuestion, FrequentlyAskedQuestion
from faithful_heart import constants


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    username = serializers.RegexField(
        regex=constants.USERNAME_REGEX,
        # min_lenght=constants.USERNAME_MIN_LENGTH,
        # max_length=constants.USERNAME_MAX_LENGTH,
        validators=[
            UniqueValidator(queryset=TelegramUser.objects.all())
        ]
    )
    name = serializers.RegexField(
        regex=constants.NAME_REGEX,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=TelegramUser.objects.all())
        ]
    )
    phone = serializers.RegexField(regex=constants.PHONE_NUMBER,)

    class Meta:
        model = TelegramUser
        fields = ('username')


class FrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка вопросов."""
    class Meta:
        model = FrequentlyAskedQuestion
        fields = ('text', 'id')


class FaqAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа на выбранный вопрос."""
    class Meta:
        model = FrequentlyAskedQuestion
        fields = ('answer',)


class UniqueQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для уникального вопроса пользователя."""
    text = serializers.CharField(max_length=constants.FAQ_MAX_LENGTH,)

    class Meta:
        model = UniqueQuestion
        fields = ('text',)
        extra_kwargs = {'text': {'required': True}}


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""
    pass
