"""
Create the application instance.
"""

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api


from api.models import db
from api.views.auth import AuthResource
from api.views.board import BoardResource
from api.views.conversation import (
    ConversationResource, MessageResource)
from api.views.user import (
    UserResource, UserRolesResource, UserWalletResource)
from api.views.welcome import WelcomeResource
from config import configurations


def create_app(configuration):
    """
    Create the flask app.
    """
    app = Flask(__name__)
    app.config.from_object(configurations[configuration])
    app_context = app.app_context()
    app_context.push()
    db.init_app(app)
    db.create_all()

    JWTManager(app)
    api = Api(app)

    api.add_resource(
        WelcomeResource,
        '/',
        '/api/v1',
        '/api/v1/'
    )

    api.add_resource(
        AuthResource,
        '/api/v1/signin',
        '/api/v1/signin/')

    api.add_resource(
        UserResource,
        '/api/v1/users',
        '/api/v1/users/',
        '/api/v1/users/<int:user_id>',
        '/api/v1/users/<int:user_id>/',
        '/api/v1/users/?name=<string:name>'
    )

    api.add_resource(
        UserWalletResource,
        '/api/v1/users/<int:user_id>/wallet',
        '/api/v1/users/<int:user_id>/wallet/')

    api.add_resource(
        UserRolesResource,
        '/api/v1/users/<int:user_id>/roles',
        '/api/v1/users/<int:user_id>/roles/')

    api.add_resource(
        BoardResource,
        '/api/v1/boards',
        '/api/v1/boards/',
        '/api/v1/boards/<int:board_id>',
        '/api/v1/boards/<int:board_id>/')

    api.add_resource(
        ConversationResource,
        '/api/v1/conversations',
        '/api/v1/conversations/',
        '/api/v1/conversations/<int:conversation_id>',
        '/api/v1/conversations/<int:conversation_id>/')

    api.add_resource(
        MessageResource,
        '/api/v1/conversations/<int:conversation_id>/messages',
        '/api/v1/conversations/<int:conversation_id>/messages/')

    return app


app = create_app('development')
