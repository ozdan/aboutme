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
    )

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

    username = Column(String(32))
    email = Column(String(64))
    password = Column(Text)

# Index('my_index', MyModel.name, unique=True)
