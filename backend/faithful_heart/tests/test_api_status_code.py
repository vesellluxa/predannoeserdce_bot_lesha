import pytest
from http import HTTPStatus
from users.models import TelegramUser



class TestStatusCodeAPI:
    @pytest.mark.django_db
    def test_users_post(self, api_client):
        data = {
            'username': 'Sveta_255',
            'chat_id': '4274875639'
        }
        url = '/api/v1/users/'
        response = api_client.post(url, data=data)
        assert response.status_code == HTTPStatus.CREATED, (
            'Проверьте, что при POST-запросе пользователя  '
            'к `/api/v1/users/` '
            ' возвращается ответ со статусом 201.'
        )


    @pytest.mark.django_db
    def test_users_update(self, admin_client, telegram_user):
        data = {
            'name': 'Svetlana',
            'surname': 'Petrova',
            'phone': '89853469506',
            'email': 'sveta-1978@mail.ru'
        }
        url = f'/api/v1/users/{telegram_user.chat_id}'
        response = admin_client.patch(url, data=data)
        # print(TelegramUser.objects.filter(chat_id=telegram_user.chat_id).first().email)
        assert response.status_code == HTTPStatus.CREATED, (
            'Проверьте, что при PATCH-запросе пользователя к '
            '`/api/v1/users/` возвращается ответ со '
            'статусом 200.'
        )

    @pytest.mark.django_db
    def test_download_users_information(self, admin_client):
        url = '/api/v1/download_user_information/'
        response = admin_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что при GET-запросе админа к '
            '`/api/v1/download_user_information/`'
            'возвращается ответ со статусом 200.'
        )

    @pytest.mark.django_db
    def test_faq(self, api_client):
        url = '/api/v1/faq/'
        response = api_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что при GET-запросе пользователя к '
            '`/api/v1/faq/` возвращается ответ со статусом 200.'
        )

    @pytest.mark.django_db
    def test_unique_question(self, admin_client):
        url = '/api/v1/unique_question/'
        data = {
            'owner': '4274875639',
            'text': 'У вас есть серые коты?'
        }
        response = admin_client.post(url, data)
        assert response.status_code == HTTPStatus.CREATED, (
            'Проверьте, что при POST-запросе пользователя к '
            '`/api/v1/unique_question/` возвращается '
            'ответ со статусом 201.'
        )
