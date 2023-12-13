from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin


class UsersView(CreateModelMixin,
               UpdateModelMixin,
               ListModelMixin,
               GenericAPIView):

    @action(detail=False, methods=['get'])
    def get_user_information(self, request):
        """Эндпойнт для выгрузки информации о пользователях."""
        pass



class FaqView(ListAPIView):
    pass


class UniqueQuestionView(CreateAPIView):
    pass


class CreateTokenView(CreateAPIView):
    pass

