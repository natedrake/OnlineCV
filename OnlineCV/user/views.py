# -*- coding: utf-8 -*-
"""User views."""
import click
from flask import (
    Blueprint, request, flash, redirect, url_for
)
from flask_apispec import (
    use_kwargs, marshal_with
)
from flask_login import (
    LoginManager, login_user, login_required, logout_user, current_user as fl_current_user
)
from OnlineCV.user.models import User
from OnlineCV.user.serializers import user_schema
from OnlineCV.decorators import templated

user_blueprint = Blueprint('user', __name__, cli_group='user', template_folder='../templates/user/')
