# -*- coding: utf-8 -*-
"""General views."""
from flask import Blueprint, render_template, jsonify, request
from OnlineCV.extensions import cache

from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import (
    jwt_required, jwt_optional, create_access_token, current_user
)
from sqlalchemy.exc import IntegrityError
from OnlineCV.database import db
from OnlineCV.exceptions import InvalidUsage
from OnlineCV.visitor.models import Visitor
from OnlineCV.visitor.serializers import visitor_schema

general_blueprint = Blueprint('general', __name__, url_prefix='/',
    template_folder='../general/')

@general_blueprint.route('/')
@cache.cached()
def index():
    Visitor(
        ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
        user_agent=request.user_agent.string
    ).save()
    return render_template('index.html', title="Resume")

@cache.cached(timeout=50)
@general_blueprint.route('/health', methods=['GET', 'POST'])
@general_blueprint.route('/health/<string:type>', methods=['POST'])
def health(type=None):
    if type == 'json':
        return jsonify(message='OK')
    else:
        return render_template('health.html', title='Health Check')
