# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hashlib import sha256
import imghdr
from wtforms import Form, StringField, TextAreaField, HiddenField, PasswordField
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired, Email, Length


strip_filter = lambda x: x.strip() if x else None


class UserUpdateForm(Form):
    first_name = StringField('Имя', [Length(min=2, max=32), DataRequired()], filters=[strip_filter])
    last_name = StringField('Фамилия', [Length(min=2, max=32), DataRequired()], filters=[strip_filter])
    biography = TextAreaField(filters=[strip_filter])
    location = StringField('Местоположение', [Length(max=50)], filters=[strip_filter])
    work = StringField('Работа', [Length(max=50)], filters=[strip_filter])
    education = StringField('Образование', [Length(max=70)], filters=[strip_filter])
    interest = StringField('Интересы', [Length(max=30)], filters=[strip_filter])
    picture = FileField('Фон профиля')

    def validate(self):
        if self.picture.data != '':
            image_type = imghdr.what(self.picture.data.file)
            if not image_type:
                self.picture.errors = ['Файл должен быть изображением']
                return False
            else:
                return super(UserUpdateForm, self).validate()
        else:
            return super(UserUpdateForm, self).validate()


class MyPasswordField(PasswordField):
    def __init__(self, label=None, validators=None, filters=tuple(),
                 description='', id=None, default=None, widget=None,
                 _form=None, _name=None, _prefix='', _translations=None,
                 _meta=None, hash_function=None):
        super(MyPasswordField, self).__init__(label, validators, filters, description, id,
            default, widget, _form, _name, _prefix, _translations, _meta)
        self.hash_function = hash_function

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.hash_function(valuelist[0]).hexdigest()
        else:
            self.data = ''


class LoginForm(Form):
    username = StringField('Ник', [Length(min=3, max=30), DataRequired()], filters=[strip_filter])
    password = MyPasswordField('Пароль', [DataRequired()], hash_function=sha256)


class AccountCreateForm(LoginForm):
    first_name = StringField('Имя', [Length(min=2, max=32), DataRequired()], filters=[strip_filter])
    last_name = StringField('Фамилия', [Length(min=2, max=32), DataRequired()], filters=[strip_filter])
    email = StringField('Email', [DataRequired(), Email()], filters=[strip_filter])


class AccountUpdateForm(LoginForm):
    email = StringField('Email', [DataRequired(), Email()], filters=[strip_filter])
