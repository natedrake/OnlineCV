# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
from OnlineCV.extensions import (
    bcrypt, cache, db, migrate, jwt, cors
)
from OnlineCV import commands, user, visitor
from OnlineCV.user.views import user_blueprint
from OnlineCV.visitor.views import visitor_blueprint
from OnlineCV.templates.general.views import general_blueprint
from OnlineCV.settings import ProdConfig
from OnlineCV.exceptions import InvalidUsage

def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app._static_folder = '../assets'
    app.config.from_object(config_object)
    register_extensions(app, config_object)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app

def register_extensions(app, config_object):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

def register_blueprints(app):
    """Register Flask blueprints."""
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(user_blueprint, origins=origins)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(visitor_blueprint)
    app.register_blueprint(general_blueprint)

def register_errorhandlers(app):
    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response
    app.errorhandler(InvalidUsage)(errorhandler)

def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.models.User,
            'Visitor': visitor.models.Visitor
        }

    app.shell_context_processor(shell_context)

def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
