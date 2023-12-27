import pytest

from users.models import TelegramUser

class TestModelFieldsValidation:

      @pytest.mark.django_db
      @pytest.mark.parametrize(
         'username, chat_id, status_code', [
            ('', '4965823419', 400),
            ('angelina56', '', 400),
            ('angelinaewdrufjdntfhgtplrdjfr8t5tf', '4965823419', 400),
            ('ola', '4965823419', 400),
            ('angelina56', '4965823419', 201),

         ]
      )
      def test_create_user_data_validation(
         self, username, chat_id, status_code, api_client
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
            ('', 'Basmanova', '79854567869', 'alla@mail.ru', 400),
            ('Irina', '', '79854567866', 'irina@mail.ru', 400),
            ('Alex', 'Basmanov', '', 'alex@mail.ru', 400),
            ('Alexander', 'Basmanov', '74951243546', '', 400),
            ('Дарья', 'Миронова', '7658е145356', 'mironova@mail.ru', 400),
            ('...///', 'Некрасова', '76586145356', 'neckrasov@mail.ru', 400),
            ('Ангелина', '..', '76586145367', 'neckrasov@mail.ru', 400),
            ('Alexander', 'Petrov', '74951243576', 'alex22@mail.ru', 200),
         ]
      )
      def test_update_user_data_validation(
         self, name, surname, phone, email, status_code, api_client
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
         self, chat_id, text, status_code, api_client
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
      @pytest.mark.parametrize(
         'username, chat_id, status_code', [
            ('angelina56', '4965823420', 400),
            ('angelina', '4965823419', 400),
            ('angelina', '4965823420', 201),
         ]
      )
      def test_unique_required_fields(
         self, username, chat_id, status_code, api_client
      ):
         url = '/api/v1/users/'
         data = {
            'username': username,
            'chat_id': chat_id
         }
         response = api_client.post(url, data=data)
         assert response.status_code == status_code, (
            'Проверьте, что при POST-запросе пользователя к '
            '`/api/v1/users/` валидация на уникальность полей '
            'выполняется правильно.'
         )
