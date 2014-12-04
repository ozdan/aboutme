# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from wtforms import Form, StringField, TextAreaField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Email, Length


strip_filter = lambda x: x.strip() if x else None


class UserUpdateForm(Form):
    first_name = StringField('Имя', [Length(min=2, max=32), DataRequired()], filters=[strip_filter])
    last_name = StringField('Фамилия', [Length(min=2, max=32), DataRequired()], filters=[strip_filter])
    biography = TextAreaField(filters=[strip_filter])
    location = StringField('Местоположение', [Length(max=50)], filters=[strip_filter])
    work = StringField('Работа', [Length(max=50)], filters=[strip_filter])
    education = StringField('Образование', [Length(max=70)], filters=[strip_filter])
    interest = StringField('Местоположение', [Length(max=30)], filters=[strip_filter])


class LoginForm(Form):
    username = StringField('Ник', [Length(min=3, max=30), DataRequired()], filters=[strip_filter])
    password = PasswordField('Пароль', [DataRequired()])


class AccountCreateForm(LoginForm):
    first_name = StringField('Имя', [Length(min=2, max=32), DataRequired()], filters=[strip_filter])
    last_name = StringField('Фамилия', [Length(min=2, max=32), DataRequired()], filters=[strip_filter])
    email = StringField('Email', [DataRequired(), Email()], filters=[strip_filter])


class AccountUpdateForm(Form):
    username = StringField('Ник', [Length(min=3, max=30), DataRequired()], filters=[strip_filter])
    email = StringField('Email', [DataRequired(), Email()], filters=[strip_filter])
    password = PasswordField('Пароль', [DataRequired()])
    id = HiddenField()
