# -*- coding: utf-8 -*-
"""General views."""
from flask import (
    Blueprint, request
)
from OnlineCV.visitor.models import Visitor
from OnlineCV.decorators import templated

general_blueprint = Blueprint('general', __name__, url_prefix='/', template_folder='../general/')


@general_blueprint.route('/', methods=('GET', 'POST'))
@templated('index.html')
def index():
    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_agent = request.user_agent.string
    Visitor(
        ip_address=ip_address,
        user_agent=user_agent
    ).save()
    return dict(title="Resume")


@general_blueprint.route('/health', methods=['GET', 'POST'])
@templated('health.html')
def health():
    return dict(title='Health Check')
