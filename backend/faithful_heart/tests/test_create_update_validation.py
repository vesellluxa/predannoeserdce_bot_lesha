import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
   'username, chat_id, status_code', [
      ('', '4965823419', 400),
      ('angelina56', '', 400),
      ('angelina56', '49658234', 400),
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
      ('', '', 'dfgs3456', '123@mail.ru', 400),
   ]
)
def test_update_user_data_validation(
   name, surname, phone, email, status_code, admin_client,
      telegram_user
):
   url = f'/api/v1/users/{telegram_user.chat_id}'
   data = {
        'name': name,
        'surname': surname,
        'phone': phone,
        'email': email,
   }
   response = admin_client.patch(url, data=data)
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
   chat_id, text, status_code, admin_client
):
   url = '/api/v1/unique_question/'
   data = {
      'owner': chat_id,
      'text': text
   }
   response = admin_client.post(url, data=data)
   assert response.status_code == status_code, (
        'Проверьте, что при POST-запросе пользователя к '
        '`/api/v1/unique_question/` валидация '
        'выполняется правильно.'
   )
