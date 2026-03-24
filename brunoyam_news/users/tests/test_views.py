from django.contrib.auth.handlers.modwsgi import check_password
from django.test import TestCase
from django.test.client import Client

from ..models import User


class SignUpViewTest(TestCase):
    def test_sign_up_view_status_code(self):
        """
        Case: Тест получения статус-кода страницы /signup/.
        Expected: Страница со статус-кодом 200.
        """
        self.client = Client()
        self.response = self.client.get('/signup/')
        self.assertEqual(self.response.status_code, 200)

    def test_sign_up_view_uses_correct_template(self):
        """
        Case: Тест используемых шаблонов страницы.
        Expected: Страницы с используемыми шаблонами signup.html и base.html.
        """
        self.client = Client()
        self.response = self.client.get('/signup/')
        self.assertTemplateUsed(self.response, 'signup.html')
        self.assertTemplateUsed(self.response, 'base.html')

    def test_sign_up_view(self):
        """
        Case: Тест создания нового пользователя с именем
        self.test_username и паролем self.test_password.
        Expected: Новый пользователь создан и авторизован.
        Произведено перенаправление на url /index/.
        """
        self.client = Client()
        self.test_username = 'test_username'
        self.test_password = 'GFGHssdsHGFGHYY443JJGBSDvvvv'
        self.response = self.client.post(
            '/signup/',
            {
                'username': self.test_username,
                'password1': self.test_password,
                'password2': self.test_password
            },
            follow=True
        )
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(
            self.response.context['user'].username,
            self.test_username
        )
        self.assertURLEqual(self.response.request['PATH_INFO'], '/index/')


class LogOutViewTest(TestCase):
    def setUp(self):
        self.username = 'TestUser1'
        self.password = 'GFGHssdsHGFGHYY443JJGBSDvvvv'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        self.client = Client()
        self.client.login(username=self.username, password=self.password)

    def test_logout_view(self):
        """
        Case: Тест выхода авторизованного пользователя.
        Expected: Пользователь вышел.
        Произведено перенаправление на url /index/.
        """
        self.response = self.client.get('/merch_category/')
        self.assertTrue(self.response.context['user'].is_authenticated)
        self.response = self.client.post(
            '/logout/',
            follow=True
        )
        self.assertFalse(self.response.context['user'].is_authenticated)
        self.assertURLEqual(self.response.request['PATH_INFO'], '/index/')


class PersonalViewTest(TestCase):
    def setUp(self):
        self.username = 'TestUser1'
        self.password = 'GFGHssdsHGFGHYY443JJGBSDvvvv'
        self.name = 'John'
        self.surname = 'Robinson'
        self.email = 'john@gmail.com'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            name=self.name,
            surname=self.surname,
            email=self.email
        )

    def test_personal_view_uses_correct_template(self):
        """
        Case: Тест используемых шаблонов страницы.
        Expected: Страницы с используемыми шаблонами personal.html и base.html.
        """
        self.client = Client()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get('/personal/')
        self.assertTemplateUsed(self.response, 'personal.html')
        self.assertTemplateUsed(self.response, 'base.html')

    def test_personal_view(self):
        """
        Case: Тест отображения личной информации пользователя.
        Expected: Отображена страница с персональными данными пользователя,
        созданного в функции setUp.
        """
        self.client = Client()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get('/personal/')
        self.assertContains(self.response, self.name)
        self.assertContains(self.response, self.surname)
        self.assertContains(self.response, self.email)


class PersonalDataChangeViewTest(TestCase):
    def setUp(self):
        self.username = 'TestUser1'
        self.password = 'GFGHssdsHGFGHYY443JJGBSDvvvv'
        self.name = 'John'
        self.surname = 'Robinson'
        self.email = 'john@gmail.com'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            name=self.name,
            surname=self.surname,
            email=self.email
        )

    def test_personal_data_change_view_uses_correct_template(self):
        """
        Case: Тест используемых шаблонов страницы.
        Expected: Страницы с используемыми шаблонами personal_data_change.html
        и base.html.
        """
        self.client = Client()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get('/personal/change/')
        self.assertTemplateUsed(self.response, 'personal_data_change.html')
        self.assertTemplateUsed(self.response, 'base.html')

    def test_personal_data_change_view(self):
        """
        Case: Тест post запроса на изменение персональных данных.
        Expected: Персональные данные изменены с созданных в setUp на
        self.new_test_name, self.new_test_surname, self.new_test_email.
        """
        self.new_test_name = 'Mark'
        self.new_test_surname = 'Benson'
        self.new_test_email = 'mark@yahoo.com'
        self.client = Client()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(
            '/personal/change/',
            {
                'name': self.new_test_name,
                'surname': self.new_test_surname,
                'email': self.new_test_email
            },
            follow=True
        )
        self.assertEqual(self.response.status_code, 200)
        self.assertURLEqual(self.response.request['PATH_INFO'], '/personal/')
        self.assertContains(self.response, self.new_test_name)
        self.assertContains(self.response, self.new_test_surname)
        self.assertContains(self.response, self.new_test_email)


class PasswordChangeView(TestCase):
    def setUp(self):
        self.username = 'TestUser1'
        self.password = 'GFGHssdsHGFGHYY443JJGBSDvvvv'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )

    def test_password_change_view_uses_correct_template(self):
        """
        Case: Тест используемых шаблонов страницы.
        Expected: Страницы с используемыми шаблонами password_change.html
        и base.html.
        """
        self.client = Client()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get('/password_change/')
        self.assertTemplateUsed(self.response, 'password_change.html')
        self.assertTemplateUsed(self.response, 'base.html')

    def test_password_change_view(self):
        """
        Case: Тест post запроса на изменение пароля.
        Expected: Пароль пользователя изменен на новый.
        """
        self.new_password = 'Bens332onFFDsdsAAAfsrr'
        self.client = Client()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(
            '/password_change/',
            {
                'old_password': self.password,
                'new_password1': self.new_password,
                'new_password2': self.new_password
            },
            follow=True
        )
        self.assertEqual(self.response.status_code, 200)
        self.assertURLEqual(
            self.response.request['PATH_INFO'],
            '/password_change/done/'
        )
        self.user = User.objects.all()[0]
        self.assertTrue(self.user.check_password(self.new_password))


class PasswordChangeDoneView(TestCase):
    def setUp(self):
        self.username = 'TestUser1'
        self.password = 'GFGHssdsHGFGHYY443JJGBSDvvvv'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )

    def test_password_change_done_view_uses_correct_template(self):
        """
        Case: Тест используемых шаблонов страницы.
        Expected: Страницы с используемыми шаблонами password_change_done.html
        и base.html.
        """
        self.client = Client()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get('/password_change/done/')
        self.assertTemplateUsed(self.response, 'password_change_done.html')
        self.assertTemplateUsed(self.response, 'base.html')