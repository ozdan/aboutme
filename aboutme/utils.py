# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy.sql import exists
from aboutme.models import DBSession, User


def unique_value_exists(form):
    username = form.data['username']
    email = form.data['email']
    result = False
    if DBSession.query(exists().where(User.username == username)).scalar():
        result = True
        form.errors['username'] = ['Пользователь с таким ником уже существует']
        form['username'].errors = ['Пользователь с таким ником уже существует']
    if DBSession.query(exists().where(User.email == email)).scalar():
        result = True
        form.errors['email'] = ['Пользователь с таким email уже существует']
        form['email'].errors = ['Пользователь с таким email уже существует']
    return result
