# -*- coding: utf-8 -*-
"""General views."""
from flask import Blueprint, render_template

general_blueprint = Blueprint('general', __name__, url_prefix='/',
    template_folder='../general/')

@general_blueprint.route('/')
def index():
    return render_template('index.html', title="Resume")
