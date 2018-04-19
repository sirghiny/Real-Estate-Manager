"""
Authorization functionality.
Allows log in of a user.
"""

from datetime import timedelta

from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from api.helpers.general import digest
from api.helpers.validation import validate_json
from api.models import User

# pylint:disable=no-self-use


class AuthResource(Resource):
    """
    Resource to handle authorization.
    """

    def post(self):
        """
        Sign a user in.
        """
        payload = request.get_json()
        required = ['email', 'password']
        result = validate_json(required, payload)
        if isinstance(result, bool) is True:
            password = digest(payload['password'])
            user = User.get(email=payload['email'])
            if isinstance(user, dict) is True:
                return {
                    'status': 'fail',
                    'data': {
                        'message': 'User does not exist.'
                    }
                }, 400
            if user.password != password:
                return {
                    'status': 'fail',
                    'data': {
                        'message': 'Wrong password.'
                    }
                }, 400
            token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(days=7)
            )
            return {
                'status': 'success',
                'data': {
                    'message': 'Welcome to Real Estate Manager!',
                    'token': token
                }
            }, 200
        return {
            'status': 'fail',
            'data': {
                'missing': result
            }
        }, 400
