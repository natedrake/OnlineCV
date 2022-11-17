# -*- coding: utf-8 -*-
"""User views."""
from flask import (
    Blueprint
)
user_blueprint = Blueprint('user', __name__, cli_group='user', template_folder='../templates/user/')
