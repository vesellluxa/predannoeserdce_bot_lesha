import os
import django
import pytest


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faithful_heart.settings')
django.setup()


# @pytest.fixture(scope='session')
# def django_db_setup():
#    from django.core.management import call_command
#    call_command('sqlmigrate')


# @pytest.fixture(scope="session")
# def test_db():
#    # Создание БД
#    db = Test_DB()
#    db.create_tables()
#    yield db
#    # Удаление БД после выполнения всех тестов
#    db.drop_tables()


@pytest.fixture()
def api_client():
   from rest_framework.test import APIClient
   return APIClient()


@pytest.fixture()
def telegram_user():
   from users.models import TelegramUser
   return TelegramUser.objects.create(username='Sveta_255', chat_id='4274875639')


@pytest.fixture()
def admin_user(django_user_model):
   return django_user_model.objects.create_superuser(username='admin', password='12345qwerty')
