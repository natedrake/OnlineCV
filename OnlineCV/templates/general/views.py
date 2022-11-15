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

@general_blueprint.route('/', methods=['GET', 'POST'])
def index():
    print(sys.executable)
    print("CACHES", CACHES, file=sys.stderr)
    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_agent = request.user_agent.string
    visitor = Visitor.query.filter_by(ip_address=ip_address, user_agent=user_agent).first()
    visits = cache.get('visits')

    if not visits:
        visits = Visitor.query.all()
        cache.set('visits', visits)

    if visits[0] != visitor:
        Visitor(
            ip_address=ip_address,
            user_agent= user_agent
        ).save()
        cache.delete('visits')

    return render_template('index.html', title="Resume")

@general_blueprint.route('/health', methods=['GET', 'POST'])
@general_blueprint.route('/health/<string:type>', methods=['POST'])
def health(type=None):
    if type == 'json':
        return jsonify(message='OK')
    else:
        return render_template('health.html', title='Health Check')
