# -*- coding: utf-8 -*-
"""Visitor views."""
from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import (
    jwt_required, jwt_optional, create_access_token, current_user
)
from sqlalchemy.exc import IntegrityError
from OnlineCV.database import db
from OnlineCV.exceptions import InvalidUsage
from .models import Visitor
from .serializers import visitor_schema

visitor_blueprint = Blueprint('visitor', __name__, template_folder='../templates/visitor/')
