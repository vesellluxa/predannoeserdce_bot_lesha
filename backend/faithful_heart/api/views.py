import csv

from aiogram import Bot, types
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.mixins import (CreateModelMixin, UpdateModelMixin,
                                   ListModelMixin, RetrieveModelMixin)

from .serializers import (UserSerializer, UniqueQuestionSerializer,
                          FaqSerializer, FaqAnswerSerializer,
                          UserUsernameSerializer)
from users.models import TelegramUser
from questions.models import UniqueQuestion, FrequentlyAskedQuestion


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
        response = Response(
            users,
            content_type='application/vnd.ms-excel; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="Пользователи.xls"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Phone', 'Username', 'Chat_id', 'Email'])
        for user in users:
            writer.writerow([user.name, user.phone, user.username,
                             user.chat_id, user.email])

        return response


class FaqView(ListModelMixin,
              RetrieveModelMixin,
              GenericAPIView):
    """Запрос на получение списка вопросов.
    Получение ответа на вопрос."""
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('is_main',)

    def get_serializer_class(self):
        if self.action in ('retrieve',):

            return FaqAnswerSerializer

        return FaqSerializer


class UniqueQuestionView(APIView):
    """Создание пользователем уникального вопроса.
    Уведомление администратора по email и в TG."""

    def post(self, request):
        serializer = UniqueQuestionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            question = serializer.validated_data.get('question')
            send_mail(f'Поступил новый вопрос', question, (ADMIN_EMAIL, ), fail_silently=False)
            bot = Bot(token=TOKEN)
            bot.send_message(chat_id=ADMIN_TG_CHAT_ID,
                text=f'Поступил новый вопрос: {question}')

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTokenView(CreateAPIView):
    """Создание ботом токена."""
    pass
