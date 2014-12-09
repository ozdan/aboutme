# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from redis import Redis
import time
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import exists
from aboutme.models import DBSession, User


def unique_value_exists(form, new=True):
    username = form.data['username']
    email = form.data['email']
    result = False
    username_query = DBSession.query(exists().where(User.username == username))
    email_query = DBSession.query(exists().where(User.email == email))
    if not new:
        username_query = username_query.filter(username != username)
        email_query = email_query.filter(username != username)
    if username_query.scalar():
        result = True
        form.errors['username'] = ['Пользователь с таким ником уже существует']
        form['username'].errors = ['Пользователь с таким ником уже существует']
    if email_query.scalar():
        result = True
        form.errors['email'] = ['Пользователь с таким email уже существует']
        form['email'].errors = ['Пользователь с таким email уже существует']
    return result


def get_image(user, width=None, height=None):
    from aboutme import store
    try:
        image = user.picture.find_thumbnail(width=width, height=height)
    except NoResultFound:
        image = user.picture.generate_thumbnail(width=width, height=height, store=store)
        image.user = user
        DBSession.flush()
    return image.locate(store=store)

connection = Redis()
ONLINE_LAST_MINUTES = 5  # корявенько здесь держать настройки, в Django для этих целей settings.py


def mark_online(user_id):
    if user_id:
        now = int(time.time())
        expires = now + (ONLINE_LAST_MINUTES * 60) + 10
        user_key = 'user_activity/%s' % user_id
        p = connection.pipeline()
        p.set(user_key, now)
        p.expireat(user_key, expires)
        p.execute()


def get_user_last_activity(user_id):
    if user_id:
        last_active = connection.get('user_activity/%s' % user_id)
        if last_active is None:
            return None
        return datetime.utcfromtimestamp(int(last_active))
