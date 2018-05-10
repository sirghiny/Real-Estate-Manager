"""
Role manipulation functionality.
"""

from flask_restful import Resource

from api.helpers.auth import token_required
from api.helpers.modelops import get_roles


class RoleResource(Resource):
    """
    View functions for roles.
    """

    @token_required
    def get(self, role_id=None):
        """
        View basic role(s) information.
        """
        result = get_roles(role_id)
        if isinstance(result, dict):
            return result, 404
        elif isinstance(result, list):
            return {
                'status': 'success',
                'data': {
                    'roles': [role.__repr__() for role in result]
                }
            }, 200
        else:
            return {
                'status': 'success',
                'data': {
                    'role': result.__repr__()
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
        result = get_roles(role_id)
        if isinstance(result, dict):
            return result, 404
        else:
            users = result.users
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
                        'role': result.view()
                    }
                }, 200
