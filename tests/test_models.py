# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt
import pytest

from OnlineCV.user.models import User
from .factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""
    def test_get_by_id(self):
        """Get user by ID."""
        user = User(username='foo', email='foo@bar.com')
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_create_at_default_to_datetime(self):
        """Test creation date."""
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory(password='myprecious')
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.check_password('myprecious')

    def test_check_password(self):
        """Check password."""
        user = User.create(username='foo', email='foo@bar.com', password='foobarbaz123')
        assert user.check_password('foobarbaz123')
        assert not user.check_password('foobaaz')
