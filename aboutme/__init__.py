from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from aboutme import views

from .models import (
    DBSession,
    Base,
    MyModel
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('register', '/register')
    config.add_route('user', '/{username}')
    config.add_route('users', '/users')
    config.add_route('guests', '/guests')
    config.scan(views)
    return config.make_wsgi_app()
