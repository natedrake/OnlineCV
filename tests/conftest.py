# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from webtest import TestApp

from OnlineCV.app import create_app
from OnlineCV.database import db as _db
from OnlineCV.settings import TestConfig

from .factories import UserFactory

@pytest.fixture(scope='function')
def app():
    """An application for the tests."""
    _app=create_app(TestConfig)

    with _app.app_context():
        _db.create_all()

    ctx=_app.test_request_context()
    ctx.push()

    yield _app

    def teardown():
        ctx.pop()

@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app"""
    return TestApp(app)

@pytest.fixture(scope='function')
def db(app):
    """A database for the tests."""
    _db.app=app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicity close the DB connection
    _db.session.close()
    _db.drop_all()

@pytest.fixture
def user(db):
    """A user for the tests."""
    class User():
        def get(self):
            muser=UserFactory(password='myprecious')
            muser.save()
            db.session.commit()
            return muser
    return User()
