import os
import django
import pytest


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.test_settings')
django.setup()

pytest_plugins = ["pytest_django"]


@pytest.fixture()
def api_client():
   from rest_framework.test import APIClient
   return APIClient()


@pytest.fixture()
def admin_user(django_user_model):
   return django_user_model.objects.create_superuser(username='admin', password='12345qwerty')
