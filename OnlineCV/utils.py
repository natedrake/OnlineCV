# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import os
from OnlineCV.user.models import User  # noqa

def jwt_identity(payload):
    return User.get_by_id(payload)

def identity_loader(user):
    return user.id

def get_test_flag():
    if os.environ.get('FLASK_TESTING') == "1":
        return True
    else:
        return False
