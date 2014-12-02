#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from paste.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import forget, remember
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'aboutme'}


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


@view_config(route_name='login')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'
    came_from = request.params.get('came_from', referrer)
    if 'form.submitted' in request.POST:
        login = request.params.get('login')
        password = request.params.get('password')
        if False:  # Find in DB
            headers = remember(request, login)
            return HTTPFound(location=came_from, headers=headers)
        message = "Неправильный логин или пароль"

    return dict(
        message=message,
        url=login_url,
        came_from=came_from,
        login=login,
        password=password
    )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    url = request.route_url('home')
    return HTTPFound(location=url, headers=headers)


@view_config(route_name='register')
def register(request):
    return Response('OK')


@view_config(route_name='user')
def user(request):
    username = request.matchdict.get('username') or None
    return Response('OK')


@view_config(route_name='users')
def users(request):
    return Response('OK')


@view_config(route_name='guests')
def guests(request):
    return Response('OK')
