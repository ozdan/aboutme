# -*- coding: utf-8
from __future__ import unicode_literals
from pyramid.paster import get_app
import unittest
from webtest import TestApp
from .fixtures import load_data
from .models import Base


class TestMyViewSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.test_app = TestApp(get_app('testing.ini'))
        Base.metadata.create_all()
        self.trans = Base.metadata.bind.connect()
        load_data()

    def tearDown(self):
        Base.metadata.drop_all()

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
