# -*- coding: utf-8 -*-
import getpass
from redis import Redis
import os
from urlparse import urlparse
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.config import Configurator
from pymongo import Connection
from sqlalchemy import engine_from_config
from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore


PATH = '/home/%s/aboutme/images' % getpass.getuser()
if not os.path.isdir(PATH):
    os.makedirs(PATH)

store = HttpExposedFileSystemStore(
    path=PATH,
    prefix='static/images/'
)


global_db_session = None
ONLINE_LAST_MINUTES = 5


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')

    global global_db_session
    config_file = global_config['__file__']
    if config_file.endswith('development.ini'):
        from .models import DBSession, Base, User
        global_db_session = DBSession
    elif config_file.endswith('testing.ini'):
        from .models import test_session, Base, User
        global_db_session = test_session

    global_db_session.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(
        settings=settings,
        authentication_policy=AuthTktAuthenticationPolicy('verysIcretW0rd')
    )
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('registration', '/registration')
    config.add_route('user', '/user/{username}')
    config.add_route('user_edit', '/user/{username}/edit')
    config.add_route('guests', '/guests')
    config.add_route('account', '/account')
    config.scan('aboutme.views')

    db_url = urlparse(settings['mongo_uri'])
    config.registry.db = Connection(
        host=db_url.hostname,
        port=db_url.port,
    )

    def add_db(request):
        db = config.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)
        return db
    config.add_request_method(add_db, 'db', reify=True)

    redis_url = urlparse(settings['redis_uri'])

    def add_redis(request):
        redis = Redis(
            host=redis_url.hostname,
            port=redis_url.port,
        )
        return redis
    config.add_request_method(add_redis, 'redis', reify=True)

    app = config.make_wsgi_app()
    app = store.wsgi_middleware(app)
    return app
