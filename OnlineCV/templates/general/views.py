# -*- coding: utf-8 -*-
"""General views."""
from flask import Blueprint, render_template, jsonify

general_blueprint = Blueprint('general', __name__, url_prefix='/',
    template_folder='../general/')

@general_blueprint.route('/')
def index():
    return render_template('index.html', title="Resume")

@general_blueprint.route('/health', methods=['GET', 'POST'])
@general_blueprint.route('/health/<string:type>', methods=['POST'])
def health(type=None):
    if type == 'json':
        return jsonify(message='OK')
    else:
        return render_template('health.html', title='Health Check')
