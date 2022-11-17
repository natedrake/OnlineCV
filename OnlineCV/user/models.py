# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
from OnlineCV.database import (
    Column, Model, SurrogatePK, db
)
from OnlineCV.extensions import bcrypt


class User(SurrogatePK, Model):
    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(100), unique=True, nullable=False)
    password_hash = Column(db.LargeBinary(128), nullable=True)
    is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    bio = Column(db.String(300), nullable=True)
    image = Column(db.String(120), nullable=True)
    token: str = ''

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password_hash = None

    def set_password(self, password):
        """Set password."""
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password_hash, value)

    def is_active(self):
        return self.is_enabled

    def __repr__(self):
        """Represent instance as a unique string."""
        return f'<User(username={self.username}, email={self.email}, password_hash={self.password_hash}, is_enabled={self.is_enabled})'
