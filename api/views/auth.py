"""
Authorization functionality.
Allows log in of a user.
"""

from datetime import timedelta

from flask import request
from flask_restful import Resource

from api.helpers.auth import create_token
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
        if isinstance(result, bool):
            password = digest(payload['password'])
            user = User.get(email=payload['email'])
            if isinstance(user, dict):
                return {
                    'status': 'fail',
                    'message': 'The user does not exist.',
                    'help': 'Ensure arguments are of existent object.'
                }, 404
            if user.password != password:
                return {
                    'status': 'fail',
                    'message': 'Wrong password.',
                    'help': 'Recover the password if necessary.'
                }, 400
            token = create_token(payload['email'])
            return {
                'status': 'success',
                'data': {
                    'message': 'Welcome to Real Estate Manager.',
                    'token': token
                }
            }, 200
        return {
            'status': 'fail',
            'message': 'Not all fields were provided.',
            'missing': result
        }, 400
