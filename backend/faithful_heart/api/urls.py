from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UsersView, FaqView, UniqueQuestionView,
                    CreateTokenView)


router_v1 = DefaultRouter()

router_v1.register(r'users', UsersView)
router_v1.register(r'faq', FaqView)
router_v1.register(r'unique_question', UniqueQuestionView)
router_v1.register(r'create_token', CreateTokenView)


urlpatterns = [
    path('v1/', include(router_v1.urls), name='api-root'),]
