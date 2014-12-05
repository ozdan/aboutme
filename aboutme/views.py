#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from hashlib import sha256
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.security import forget, remember
from pyramid.view import view_config, notfound_view_config
from sqlalchemy.orm.exc import NoResultFound

from aboutme.forms import LoginForm, AccountCreateForm, AccountUpdateForm, UserUpdateForm
from aboutme.utils import unique_value_exists

from .models import (
    DBSession,
    User,
    )


@view_config(route_name='home')
def home(request):
    if request.authenticated_userid:
        user_list = DBSession.query(User).all()
        dct = {'user_list': user_list}
        return render_to_response('templates/users.mako', dct, request=request)
    else:
        return render_to_response('templates/index.mako', {}, request=request)


@view_config(route_name='login', renderer='templates/login.mako')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'
    came_from = request.params.get('came_from', referrer)
    message = ''
    form = LoginForm(request.POST)
    if request.method == 'POST' and form.validate():
        username = request.params.get('username')
        password = request.params.get('password')
        user = DBSession.query(User).filter_by(username=username).one()
        if user and sha256(password).hexdigest() == user.password:
            headers = remember(request, username)
            return HTTPFound(location=came_from, headers=headers)
        message = "Неправильный ник или пароль"

    return {'form': form, 'message': message}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    url = request.route_url('home')
    return HTTPFound(location=url, headers=headers)


@view_config(route_name='registration', renderer='templates/registration.mako')
def registration(request):
    form = AccountCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        if not unique_value_exists(form):
            new_user = User()
            form.data['password'] = sha256(form.data['password']).hexdigest()  # грязно
            form.populate_obj(new_user)
            DBSession.add(new_user)
            headers = remember(request, form.data['username'])
            return HTTPFound(location=request.route_url('home'), headers=headers)
    return {'form': form}


@view_config(route_name='user', renderer='templates/user.mako')
def user(request):
    username = request.matchdict.get('username')
    try:
        user = DBSession.query(User).filter_by(username=username).one()
    except NoResultFound:
        raise HTTPNotFound()
    return {'user': user}


@view_config(route_name='guests')
def guests(request):
    return Response('OK')


@notfound_view_config(renderer='templates/404.mako')
def not_found(request):
    request.response.status = 404
    return {}


@view_config(route_name='account', renderer='templates/account.mako')
def account(request):
    old_user = DBSession.query(User).filter_by(username=request.authenticated_userid).one()
    form = AccountUpdateForm(request.POST, old_user)
    if request.method == 'POST' and form.validate():
        if not unique_value_exists(form, False):
            form.data['password'] = sha256(form.data['password']).hexdigest()
            form.populate_obj(old_user)
            DBSession.add(old_user)
            headers = remember(request, form.data['username'])
            return HTTPFound(location=request.route_url('home'), headers=headers)
    return {'form': form}


@view_config(route_name='user_edit', renderer='templates/user_edit.mako')
def edit_user(request):
    username = request.matchdict.get('username')
    if username != request.authenticated_userid:
        return HTTPFound(location=request.route_url('user', username=username))
    old_user = DBSession.query(User).filter_by(username=username).one()
    form = UserUpdateForm(request.POST, old_user)
    if request.method == 'POST' and form.validate():
        form.populate_obj(old_user)
        DBSession.add(old_user)
        return HTTPFound(location=request.route_url('user', username=username))
    return {'form': form}
