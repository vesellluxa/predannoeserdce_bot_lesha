from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import (CreateModelMixin, UpdateModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from rest_framework_simplejwt.token_blacklist.models import (BlacklistedToken,
                                                             OutstandingToken)
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (UserSerializer, UniqueQuestionSerializer,
                          FrequentlyAskedQuestionSerializer,
    # FrequentlyAskedQuestionAnswerSerializer,
                          UserCreateSerializer)
from users.models import TelegramUser
from questions.models import UniqueQuestion, FrequentlyAskedQuestion
from .api_service import (export_users_excel, send_email_to_admin,
                          send_tg_notification_to_admin)


class UsersViewSet(
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet
):
    """Регистрация и обновление пользователей."""
    queryset = TelegramUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post', 'patch', ]

    def get_serializer_class(self):
        if self.action in ('create',):
            return UserCreateSerializer
        return UserSerializer


class DownloadUserInformationView(
    GenericViewSet
):
    """Эндпойнт для выгрузки информации о пользователях в Excel."""
    queryset = TelegramUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        export_users_excel(queryset)
        return Response(serializer.data)


class FrequentlyAskedQuestionView(
    ListModelMixin,
    GenericViewSet
):
    """Запрос на получение списка вопросов.
    Получение ответа на вопрос."""
    queryset = FrequentlyAskedQuestion.objects.filter(is_relevant=True)
    serializer_class = FrequentlyAskedQuestionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category',)


class UniqueQuestionView(
    CreateAPIView,
    GenericViewSet
):
    """Создание пользователем уникального вопроса.
    Уведомление администратора по email и в Telegram."""
    queryset = UniqueQuestion.objects.all()
    serializer_class = UniqueQuestionSerializer

    def perform_create(self, serializer):
        serializer.save()
        question = serializer.validated_data.get('text')
        send_email_to_admin(question)
        send_tg_notification_to_admin(question)


class APILogoutView(
    APIView
):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "Вы вышли из системы"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "Вы вышли из системы"})


class PingPongView(APIView):
    """Проверка доступности сервера"""

    def get(self, request):
        return Response({'response': 'pong'}, status=status.HTTP_200_OK)
