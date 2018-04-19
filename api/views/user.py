"""
User manipulation functionality.
"""

from flask import request
from flask_restful import Resource

from api.helpers.auth import token_required
from api.helpers.general import digest
from api.helpers.validation import validate_json
from api.models import Role, User, Wallet

# pylint:disable=no-self-use


class UserResource(Resource):
    """
    View functions for users.
    """

    def post(self):
        """
        Create a new user.
        """
        payload = request.get_json()
        required = ['email', 'name', 'password', 'phone_number']
        result = validate_json(required, payload)
        if isinstance(result, bool) is True:
            new_user = User(
                name=payload['name'],
                phone_number=payload['phone_number'],
                email=payload['email'],
                password=digest(payload['password'])
            )
            basic_role = Role.get(title='basic')
            new_wallet = Wallet()
            new_user.insert('roles', [basic_role])
            new_user.insert('wallet', new_wallet)
            new_user_id = new_user.save()
            return {
                'status': 'success',
                'message': 'User with id {} was created.'.format(new_user_id)
            }, 201
        return {
            'status': 'fail',
            'data': {
                'missing': result
            }
        }, 400

    @token_required
    def get(self, user_id=None):
        """
        View a user's information.
        """
        if user_id:
            user = User.view_public(user_id=user_id)
            if 'id' in user:
                return {
                    'status': 'success',
                    'data': user
                }, 200
            return {
                'status': 'fail',
                'message': 'The user does not exist.',
                'help': 'Ensure arguments are of existent objects and unique.'
            }, 404
        elif request.args.get('name'):
            name = request.args.get('name')
            users = User.search(name=name)
            if isinstance(users, dict) is False:
                return {
                    'status': 'success',
                    'data': {
                        'users': [User.view_public(user.id) for user in users]
                    }
                }, 200
            return {
                'status': 'fail',
                'message': 'No users with the name in the database.'
            }, 404
        users = User.get_all()
        if isinstance(users, dict) is False:
            users = [User.view_public(user_id=user.id) for user in users]
            return {
                'status': 'success',
                'data': {
                    'users': users
                }
            }, 200
        return {
            'status': 'fail',
            'message': 'No users in the database.'
        }, 404


class UserWalletResource(Resource):
    """
    View functions for user's wallet.
    """

    def get(self, user_id):
        """
        View a user's wallet.
        """
        user = User.get(id=user_id)
        if isinstance(user, dict):
            return {
                'status': 'fail',
                'message': 'The user does not exist.',
                'help': 'Ensure arguments are of existent objects and unique.'
            }, 404
        else:
            wallet = user.wallet.view()
            return {
                'status': 'success',
                'data': {
                    'wallet': wallet
                }
            }, 200


class UserRolesResource(Resource):
    """
    View functions for user's roles.
    """

    def get(self, user_id):
        """
        View a user's roles.
        """
        user = User.get(id=user_id)
        if isinstance(user, dict):
            return {
                'status': 'fail',
                'message': 'The user does not exist.',
                'help': 'Ensure arguments are of existent objects and unique.'
            }, 404
        else:
            roles = [role.view() for role in user.roles]
            return {
                'status': 'success',
                'data': {
                    'roles': roles
                }
            }, 200
