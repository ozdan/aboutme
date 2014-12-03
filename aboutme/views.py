#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from paste.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.security import forget, remember
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from aboutme.forms import LoginForm

from .models import (
    DBSession,
    User,
    )


@view_config(route_name='home')
def home(request):
    if request.authenticated_userid:
        return render_to_response('templates/users.mako', {}, request=request)
    else:
        return render_to_response('templates/index.mako', {}, request=request)
    # try:
    #     one = DBSession.query(User).filter(User.name == 'one').first()
    # except DBAPIError:
    #     return Response(conn_err_msg, content_type='text/plain', status_int=500)
    # return {'one': one, 'project': 'aboutme'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_aboutme_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""


@view_config(route_name='login', renderer='templates/login.mako')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'
    came_from = request.params.get('came_from', referrer)
    # message = ''
    # login = ''
    # password = ''
    form = LoginForm(request.POST)
    if request.method == 'POST' and form.validate():
        login = request.params.get('login')
        password = request.params.get('password')
        if False:  # Find in DB
            headers = remember(request, login)
            return HTTPFound(location=came_from, headers=headers)
        message = "Неправильный логин или пароль"

    return {'form': form}

    # return render_to_response(
    #     'templates/login.mako',
    #     {'form': form},
    #     request=request
    # )
    # return dict(
    #     message=message,
    #     url=login_url,
    #     came_from=came_from,
    #     login=login,
    #     password=password
    # )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    url = request.route_url('home')
    return HTTPFound(location=url, headers=headers)


@view_config(route_name='registration')
def registration(request):
    return Response('OK')


@view_config(route_name='user')
def user(request):
    username = request.matchdict.get('username') or None
    dct = dict(username=username)
    return render_to_response('templates/user.mako', dct, request=request)


@view_config(route_name='guests')
def guests(request):
    return Response('OK')


@view_config(route_name='check_username')
def check_username(request):
    status = 'ok'
    username = request.GET.get('username')
    if DBSession.query(User).filter_by(username=username).exists():
        status = 'error'
    return {'status': status}
