# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship)
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_imageattach.entity import image_attachment, Image

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(32))
    last_name = Column(String(32))
    biography = Column(Text)
    location = Column(String(50))
    work = Column(String(50))
    education = Column(String(70))
    interest = Column(String(30))

    username = Column(String(32), unique=True)
    email = Column(String(64), unique=True)
    password = Column(Text)
    picture = image_attachment('UserPicture')


class UserPicture(Base, Image):
    __tablename__ = 'user_picture'
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    user = relationship(User)

# Index('my_index', MyModel.name, unique=True)
