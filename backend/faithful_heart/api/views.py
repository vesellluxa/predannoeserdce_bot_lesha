import asyncio

from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.mixins import (CreateModelMixin, UpdateModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from .serializers import (UserSerializer, UniqueQuestionSerializer,
                          FrequentlyAskedQuestionSerializer, FaqAnswerSerializer,
                          UserUsernameSerializer)
from users.models import TelegramUser
from questions.models import UniqueQuestion, FrequentlyAskedQuestion
from .api_service import (export_users_excel, send_email_to_admin,
                          send_tg_notification_to_admin)


class UsersView(CreateModelMixin,
                UpdateModelMixin,
                GenericAPIView):
    """Регистрация и обновление пользователей."""
    queryset = TelegramUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=False,
            url_path='download_user_information',
            permission_classes=(IsAdminUser,))
    def download_user_information(self, request):
        """Эндпойнт для выгрузки информации о пользователях в Excel."""
        users = TelegramUser.objects.all()
        export_users_excel(users)

        return response


class FrequentlyAskedQuestionView(
        ListModelMixin,
        RetrieveModelMixin,
        GenericAPIView):
    """Запрос на получение списка вопросов.
    Получение ответа на вопрос."""
    queryset = FrequentlyAskedQuestion.objects.all()
    serializer_class = FrequentlyAskedQuestionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('is_main',)

    def get_serializer_class(self):
        if self.action in ('retrieve',):

            return FaqAnswerSerializer

        return FrequentlyAskedQuestionSerializer


class UniqueQuestionView(CreateAPIView):
    """Создание пользователем уникального вопроса.
    Уведомление администратора по email и в Telegram."""
    queryset = UniqueQuestion.objects.all()
    serializer_class = UniqueQuestionSerializer

    def perform_create(self, serializer):
        serializer.save()
        question = serializer.validated_data.get('question')
        send_email_to_admin(question)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_tg_notification_to_admin(question))


class CreateTokenView(CreateAPIView):
    """Создание ботом токена."""
    pass
