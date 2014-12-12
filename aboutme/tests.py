# -*- coding: utf-8
from __future__ import unicode_literals
from pyramid.paster import get_app
from subprocess import PIPE, Popen, call
import unittest
from webtest import TestApp
from webtest.app import AppError
from aboutme.fixtures import TEST_USERNAME, TEST_PASSWORD
from .fixtures import load_data
from .models import Base, test_session, User


class TestMyViewSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.test_app = TestApp(get_app('testing.ini'))
        Base.metadata.create_all()
        self.redis_server = Popen(["redis-server", "--port 63790"], stdout=PIPE)
        load_data()

    def tearDown(self):
        test_session.remove()
        Base.metadata.drop_all()
        self.redis_server.kill()
        # call(['rm', 'testing.db', 'testing.db-journal'])

    def not_authenticated(self, response):
        self.assertNotIn('Редактировать страницу', response.html.text)
        self.assertNotIn('Настройки аккаунта', response.html.text)
        self.assertNotIn('Гости', response.html.text)
        self.assertNotIn('Выйти', response.html.text)

    def authenticated(self, response):
        self.assertIn('Редактировать страницу', response.html.text)
        self.assertIn('Настройки аккаунта', response.html.text)
        self.assertIn('Гости', response.html.text)
        self.assertIn('Выйти', response.html.text)

    def test_index_without_login(self):
        res = self.test_app.get('/')
        self.assertIn('войдите', res.html.text)
        self.assertIn('зарегистрируйтесь', res.html.text)
        self.not_authenticated(res)

    def test_registration_empty(self):
        res = self.test_app.post('/registration', {})
        self.not_authenticated(res)
        error_string = 'This field is required'
        self.assertEqual(res.html.text.count(error_string), 5)

    def test_registration_exists(self):
        user = test_session.query(User).first()
        post_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'password': 'pass'
        }
        res = self.test_app.post('/registration', post_data)
        self.not_authenticated(res)
        self.assertIn('Пользователь с таким ником уже существует', res.html.text)
        self.assertIn('Пользователь с таким email уже существует', res.html.text)

    def test_registration_good(self):
        username = 'new_username'
        first_name = 'new_first_name'
        last_name = 'new_last_name'
        post_data = {
            'username': username,
            'email': 'new@email.com',
            'first_name': first_name,
            'last_name': last_name,
            'password': 'pass'
        }
        res = self.test_app.post('/registration', post_data)
        self.assertEqual(302, res.status_code)
        self.assertIn(username, res.location)
        res1 = res.follow()
        self.authenticated(res1)
        self.assertIn('Это ж я...', res1.html.text)
        self.assertIn(first_name, res1.html.text)
        self.assertIn(last_name, res1.html.text)

    def test_login_wrong(self):
        post_data = {
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD + '1'
        }
        res = self.test_app.post('/login', post_data)
        self.assertIn('Неправильный ник или пароль', res.html.text)
        self.not_authenticated(res)
        post_data1 = {
            'username': TEST_USERNAME + '1',
            'password': TEST_PASSWORD
        }
        res1 = self.test_app.post('/login', post_data1)
        self.assertIn('Неправильный ник или пароль', res1.html.text)

    def test_login_good_and_logout(self):
        post_data = {
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD
        }
        res = self.test_app.post('/login', post_data)
        self.assertEqual(302, res.status_code)
        self.authenticated(res.follow())
        res1 = self.test_app.get('/user/' + TEST_USERNAME)
        self.assertIn('Online', res1.html.text)
        res2 = self.test_app.get('/logout')
        self.assertEqual(302, res.status_code)
        self.not_authenticated(res2.follow())

    def test_404(self):
        try:
            self.test_app.get('/not_found_url' + TEST_USERNAME)
        except AppError as err:
            self.assertIn('404', err.message)

    def test_user_not_exists(self):
        try:
            self.test_app.get('/user/not_exists_user')
        except AppError as err:
            self.assertIn('404', err.message)

# И так далее. Еще следует провести тестирование редактирования пользовательских данных,
# редактирования аккаунта, загрузки фонового фото и наличие его на странице пользователя,
# загрузки файла не графического формата, просмотра гостей когда там никого не было и когда кто-то был
