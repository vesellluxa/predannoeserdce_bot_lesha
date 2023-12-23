from rest_framework import serializers

from users.models import TelegramUser
from questions.models import UniqueQuestion, FrequentlyAskedQuestion
from faithful_heart import constants


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания первой записи пользователя."""
    username = serializers.RegexField(
        regex=constants.USERNAME_REGEX,
        min_length=constants.USERNAME_MIN_LENGTH,
        max_length=constants.USERNAME_MAX_LENGTH,
        validators=[
            UniqueValidator(queryset=TelegramUser.objects.all())
        ]
    )

    class Meta:
        model = TelegramUser
        fields = ('username', 'chat_id', )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления данных пользователя."""
    name = serializers.RegexField(
        regex=constants.NAME_REGEX,
        min_length=constants.NAME_MIN_LENGTH,
        max_length=constants.NAME_MAX_LENGTH
    )
    surname = serializers.RegexField(
        regex=constants.NAME_REGEX,
        min_length=constants.NAME_MIN_LENGTH,
        max_length=constants.NAME_MAX_LENGTH
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=TelegramUser.objects.all())
        ]
    )
    phone = serializers.RegexField(regex=constants.PHONE_NUMBER,)
    chat_id = serializers.RegexField(
        regex=constants.PHONE_NUMBER,
        max_length=constants.CHAT_ID_LENGTH)

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
    text = serializers.CharField(max_length=constants.FAQ_MAX_LENGTH,)
    owner = TelegramUser

    class Meta:
        model = UniqueQuestion
        fields = ('text', 'owner', )
        lookup_field = 'chat_id'


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""
    pass
