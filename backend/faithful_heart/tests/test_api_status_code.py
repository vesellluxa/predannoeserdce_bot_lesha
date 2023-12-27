import pytest
from http import HTTPStatus
from users.models import TelegramUser


class TestStatusCodeAPI:

    def obtain_token(self, api_client, admin_user):
        url = '/api/v1/obtain_token/'
        data = {
            'username': admin_user.username,
            'password': '12345qwerty'
        }
        response = api_client.post(url, data=data)
        return response.data['access']

    @pytest.mark.django_db
    def test_users_post(self, api_client, headers):
        data = {
            'username': 'Sveta_255',
            'chat_id': '4274875639'
        }
        url = '/api/v1/users/'
        response = api_client.post(url, data=data, headers=headers)
        assert response.status_code == HTTPStatus.CREATED, (
            'Проверьте, что при POST-запросе пользователя  '
            'к `/api/v1/users/` '
            ' возвращается ответ со статусом 201.'
        )
        print(TelegramUser.objects.all())


    @pytest.mark.django_db
    def test_users_update(self, api_client, headers):
        data = {
            'name': 'Svetlana',
            'surname': 'Petrova',
            'phone': '89853469506',
            'email': 'sveta-1978@mail.ru'
        }
        user = TelegramUser.objects.create(username='sveta_088', chat_id='4274875640')
        chat_id = user.chat_id
        url = f'/api/v1/users/{chat_id}/'
        response = api_client.patch(url, data=data, headers=headers, follow=True)
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что при PATCH-запросе пользователя к '
            '`/api/v1/users/` возвращается ответ со '
            'статусом 200.'
        )

    @pytest.mark.django_db
    def test_download_users_information(self, api_client, admin_user):
        token = self.obtain_token(api_client, admin_user)
        headers = { "Authorization": f"Bearer {token}" }
        url = '/api/v1/download_user_information/'
        response = api_client.get(url, headers=headers)
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что при GET-запросе админа к '
            '`/api/v1/download_user_information/`'
            'возвращается ответ со статусом 200.'
        )

    @pytest.mark.django_db
    def test_faq(self, api_client, headers):
        url = '/api/v1/faq/'
        response = api_client.get(url, headers=headers)
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что при GET-запросе пользователя к '
            '`/api/v1/faq/` возвращается ответ со статусом 200.'
        )

    @pytest.mark.django_db
    def test_unique_question(self, api_client, headers):
        url = '/api/v1/unique_question/'
        owner = TelegramUser.objects.create(username='23vasja', chat_id='4987569475')
        data = {
            'owner': owner.chat_id,
            'text': 'У вас есть серые коты?'
        }
        response = api_client.post(url, data=data, headers=headers)
        assert response.status_code == HTTPStatus.CREATED, (
            'Проверьте, что при POST-запросе пользователя к '
            '`/api/v1/unique_question/` возвращается '
            'ответ со статусом 201.'
        )
