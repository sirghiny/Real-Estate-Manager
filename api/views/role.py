"""
Role manipulation functionality.
"""

from flask import request
from flask_restful import Resource

from api.helpers.auth import token_required
from api.helpers.validation import validate_json
from api.models import Role, User


class RoleResource(Resource):
    """
    View functions for roles.
    """

    @token_required
    def get(self, role_id=None):
        """
        View basic role(s) information.
        """
        roles = Role.get_all()
        if isinstance(roles, dict):
            return {
                'status': 'fail',
                'message': 'There are no roles in the system.',
                'help': 'Ensure roles are seeded.'
            }, 404
        else:
            if role_id:
                try:
                    role = [role.view() for role in roles][0]
                    return {
                        'status': 'success',
                        'data': {
                            'role': role
                        }
                    }, 200
                except IndexError:
                    return {
                        'status': 'fail',
                        'message': 'The role does not exist.',
                        'help': 'Ensure role_id is existent.'
                    }, 404
            else:
                return {
                    'status': 'success',
                    'data': {
                        'roles': [role.view() for role in roles]
                    }
                }, 200


class RoleUsersResource(Resource):
    """
    View functions for a role's users.
    """

    @token_required
    def get(self, role_id):
        """
        View the user's of a role.
        """
        role = Role.get(id=role_id)
        if isinstance(role, dict):
            return {
                'status': 'fail',
                'message': 'The role does not exist.',
                'help': 'Ensure role_id is existent.'
            }, 404
        else:
            users = role.users
            if not users:
                return {
                    'status': 'fail',
                    'message': 'The role has no users.',
                    'help': 'Have an admin add users to the role.'
                }, 404
            else:
                return {
                    'status': 'success',
                    'data': {
                        'role': role.view(),
                        'users': [user.view_public() for user in users]
                    }
                }, 200
