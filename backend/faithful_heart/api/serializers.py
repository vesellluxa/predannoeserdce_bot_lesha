from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.validators import UniqueValidator

from users.models import TelegramUser
from questions.models import UniqueQuestion, FrequentlyAskedQuestion


class UserSerializer(ModelSerializer):
    """Сериал. пользователя."""
    username = serializers.RegexField(
        regex=USERNAME_REGEX,
        min_lenght=settings.USERNAME_MIN_LENGTH,
        max_length=USERNAME_MAX_LENGTH,
        validators=[
            UniqueValidator(queryset=TelegramUser.objects.all())
        ]
    )
    name = serializers.RegexField(
        regex=NAME_REGEX,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=TelegramUser.objects.all())
        ]
    )
    phone = serializers.RegexField(regex=PHONE_NUMBER,)

    class Meta:
        model = TelegramUser
        fields = ('username')


class FrequentlyAskedQuestionSerializer(ModelSerializer):
    """Сериал. для получения списка вопросов."""
    class Meta:
        model = FrequentlyAskedQuestion
        fields = ('text',)


class FaqAnswerSerializer(ModelSerializer):
    """Сериал. для ответа на выбранный вопрос."""
    class Meta:
        model = FrequentlyAskedQuestion
        fields = ('answer',)


class UniqueQuestionSerializer(ModelSerializer):
    text = serializers.CharField(max_length=FAQ_MAX_LENGTH,)

    class Meta:
        model = UniqueQuestion
        fields = ('text',)


class TokenSerializer(Serializer):
    """Сериалайзер токена."""
    pass
