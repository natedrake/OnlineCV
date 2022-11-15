# -*- coding: utf-8 -*-
"""Visitor views."""
from flask import Blueprint, request, render_template
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import (
    jwt_required, jwt_optional, create_access_token, current_user
)
from sqlalchemy.exc import IntegrityError
from OnlineCV.database import db
from OnlineCV.exceptions import InvalidUsage
from OnlineCV.extensions import cache
from OnlineCV.visitor.models import Visitor
from OnlineCV.visitor.serializers import visitor_schema

visitor_blueprint = Blueprint('visitor', __name__, template_folder='../templates/visitor/')

@visitor_blueprint.route('/visitors', methods=['GET',])
def get_visitors():
    visits = cache.get('visits')
    if not visits:
        visits = Visitor.query.order_by(-Visitor.id).limit(10).all()
        cache.set('visits', visits, 3600)
    return render_template('visits.html', title='Recent Visitors', visits=visits)

@cache.memoize()
def get_all_visits():
    return Visitor.query.all()
