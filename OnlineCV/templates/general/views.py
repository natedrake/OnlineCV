# -*- coding: utf-8 -*-
"""General views."""
from flask import (
    Blueprint, render_template, jsonify, request
)
from flask_apispec import (
    use_kwargs, marshal_with
)
from flask_jwt_extended import (
    jwt_required, jwt_optional, create_access_token, current_user
)
from sqlalchemy.exc import IntegrityError
from OnlineCV.database import db
from OnlineCV.extensions import cache
from OnlineCV.exceptions import InvalidUsage
from OnlineCV.visitor.models import Visitor
from OnlineCV.visitor.serializers import visitor_schema
from OnlineCV.decorators import templated

general_blueprint = Blueprint('general', __name__, url_prefix='/',
    template_folder='../general/')

@general_blueprint.route('/', methods=('GET', 'POST'))
@templated('index.html')
def index():
    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_agent = request.user_agent.string
    Visitor(
        ip_address=ip_address,
        user_agent= user_agent
    ).save()
    return dict(title="Resume")

@general_blueprint.route('/health', methods=['GET', 'POST'])
@templated('health.html')
def health(type=None):
    return dict(title='Health Check')
