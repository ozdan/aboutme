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
from transaction._manager import ThreadTransactionManager
from transaction._transaction import Transaction

from zope.sqlalchemy import ZopeTransactionExtension


class TestTransactionManager(ThreadTransactionManager):
    def get(self):
        '''
        при сохранении self._txn = Transaction(self._synchs, self)
        сносятся фикстуры перед самым вызовом self.test_app.get() или post()
        :return:
        '''
        return Transaction(self._synchs, self)
test_session = scoped_session(
    sessionmaker(
        extension=ZopeTransactionExtension(transaction_manager=TestTransactionManager())
    )
)

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
