"""
User manipulation functionality.
"""

from flask import request
from flask_restful import Resource

from api.helpers.auth import token_required, view_token
from api.helpers.general import digest
from api.helpers.modelops import (
    get_user, get_users, search_users, update_resource)
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
            new_user.insert('roles', basic_role)
            new_user.insert('wallet', new_wallet)
            new_user_id = new_user.save()
            return {
                'status': 'success',
                'message': 'User with id {} was created.'.format(new_user_id)
            }, 201
        return {
            'status': 'fail',
            'message': 'Not all fields were provided.',
            'missing': result
        }, 400

    @token_required
    def get(self, user_id=None):
        """
        View a user's information.
        """
        if request.args.get('q'):
            result = search_users(request.args.get('q'))
            if 'message' in result:
                return result, 404
            else:
                return result, 200
        else:
            result = get_user(request, user_id)
            if isinstance(result, dict):
                return result, 404
            else:
                return {
                    'status': 'success',
                    'data': result.__repr__()
                }, 200

    def patch(self):
        """
        Edit a user's information.
        """
        result = get_user(request)
        if isinstance(result, dict):
            return result, 404
        else:
            update_result = update_resource(request, result)
            if isinstance(update_result, bool):
                updated_user = User.get(id=view_token(
                    request.headers.get('Authorization'))['id'])
                return {
                    'status': 'success',
                    'data': {'user': updated_user.view()}
                }, 200
            else:
                return update_result, 400

    def delete(self):
        """
        Delete a user.
        """
        result = get_user(request)
        if isinstance(result, dict):
            return result, 404
        else:
            user_id = view_token(
                request.headers.get('Authorization'))['id']
            result.delete()
            return {
                'status': 'success',
                'message': 'User with id {} has been deleted.'.format(user_id)
            }, 200


class UsersResource(Resource):
    """
    View functions for users in multiple numbers.
    """

    def get(self):
        """
        Get several users.
        """
        result = get_users()
        if 'message' in result:
            return result, 404
        else:
            return result, 200


class UserBoardsResource(Resource):
    """
    View functions for a user's boards.
    """

    @token_required
    def get(self, user_id):
        """
        View a user's boards.
        """
        result = get_user(request, user_id)
        if isinstance(result, dict):
            return result, 404
        else:
            boards = result.boards
            if not boards:
                return {
                    'status': 'fail',
                    'message': 'The user is not in any boards.',
                    'help': 'Suggest a board if necessary.'
                }, 404
            else:
                return {
                    'status': 'success',
                    'data': {'boards': [board.view() for board in boards]}
                }, 200


class UserRolesResource(Resource):
    """
    View functions for user's roles.
    """

    @token_required
    def get(self, user_id):
        """
        View a user's roles.
        """
        result = get_user(request, user_id)
        if isinstance(result, dict):
            return result, 404
        else:
            return {
                'status': 'success',
                'data': {'roles': [role.__repr__() for role in result.roles]}
            }, 200


class UserWalletResource(Resource):
    """
    View functions for user's wallet.
    """

    @token_required
    def get(self):
        """
        View a user's wallet.
        """
        result = get_user(request)
        if isinstance(result, dict):
            return result, 404
        else:
            wallet = result.wallet.view()
            return {
                'status': 'success',
                'data': {'wallet': wallet}
            }, 200
