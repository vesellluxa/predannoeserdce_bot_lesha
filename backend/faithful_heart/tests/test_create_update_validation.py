import pytest

from users.models import TelegramUser


@pytest.mark.django_db
@pytest.mark.parametrize(
   'username, chat_id, status_code', [
      ('', '4965823419', 400),
      ('angelina56', '', 400),
      ('angelinaewdrufjdntfhgtplrdjfr8t5tfujhdnsddckfjtfhdxnsdherfjswkdjfr',
         '4965823419', 400),
      ('ola', '4965823419', 400),
      ('angelina56', '4965823419', 201),

   ]
)
def test_create_user_data_validation(
   username, chat_id, status_code, api_client
):
   url = '/api/v1/users/'
   data = {
       'username': username,
       'chat_id': chat_id
   }
   response = api_client.post(url, data=data)
   assert response.status_code == status_code, (
        'Проверьте, что при POST-запросе пользователя к '
        '`/api/v1/users/` валидация данных '
        'выполняется правильно.'
   )


@pytest.mark.django_db
@pytest.mark.parametrize(
   'name, surname, phone, email, status_code', [
# здесь я допишу параметры для проверки
      ('', 'Basmanova', '79854567869', 'alla@mail.ru', 400),
   ]
)
def test_update_user_data_validation(
   name, surname, phone, email, status_code, api_client,
      telegram_user
):
   user = TelegramUser.objects.create(username='675_andrey', chat_id='4837345475')
   chat_id = user.chat_id
   url = f'/api/v1/users/{chat_id}/'
   data = {
        'name': name,
        'surname': surname,
        'phone': phone,
        'email': email,
   }
   response = api_client.patch(url, data=data, follow=True)
   assert response.status_code == status_code, (
        'Проверьте, что при PATCH-запросе пользователя к '
        '`/api/v1/users/` валидация данных '
        'выполняется правильно.'
   )


@pytest.mark.django_db
@pytest.mark.parametrize(
   'chat_id, text, status_code', [
      ('', 'Здравствуйте, котик Мурзик еще в наличии?', 400),
      ('4274875639', '', 400),
      ('4274875639', 'Здравствуйте, котик Мурзик еще в наличии?', 201),
   ]
)
def test_unique_question_data_validation(
   chat_id, text, status_code, api_client
):
   url = '/api/v1/unique_question/'
   data = {
      'owner': chat_id,
      'text': text
   }
   response = api_client.post(url, data=data)
   assert response.status_code == status_code, (
        'Проверьте, что при POST-запросе пользователя к '
        '`/api/v1/unique_question/` валидация '
        'выполняется правильно.'
   )

@pytest.mark.django_db
def test_unique_required_fields(api_client):
   url = '/api/v1/users/'
   data = {
       'username': 'angelina56',
       'chat_id': '4965823419'
   }
   response = api_client.post(url, data=data)
   assert response.status_code == 400, (
        'Проверьте, что при POST-запросе пользователя к '
        '`/api/v1/users/` валидация на уникальность полей '
        'выполняется правильно.'
   )
