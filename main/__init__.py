"""Create the application instance."""

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api


from api.models import db

from .config import configurations
from .resources import add_resources


def create_app(configuration):
    """Create the flask app."""
    app = Flask(__name__)
    app.config.from_object(configurations[configuration])
    app_context = app.app_context()
    app_context.push()
    db.init_app(app)
    db.create_all()

    JWTManager(app)
    api = Api(app)
    add_resources(api)

    return app


app = create_app('development')
