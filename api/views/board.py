"""
Board manipulation functionality.
"""

from flask import request
from flask_restful import Resource


from api.helpers.validation import validate_json
from api.models import Board, User


class BoardResource(Resource):
    """
    View functions for boards.
    """

    def get(self, board_id=None):
        """
        View a board.
        """
        if board_id:
            board = Board.get(id=board_id)
            if isinstance(board, dict):
                return {
                    'status': 'fail',
                    'message': 'The board does not exist.',
                    'help': 'Ensure board_id is of an existent board.'
                }, 404
            else:
                return {
                    'status': 'success',
                    'data': {
                        'board': board.view()
                    }
                }, 200
        else:
            boards = Board.get_all()
            if isinstance(boards, dict):
                return {
                    'status': 'fail',
                    'message': 'No boards exist.',
                    'help': 'Ensure there are boards in the database.'
                }, 404
            else:
                return {
                    'status': 'success',
                    'data': {
                        'boards': [board.view() for board in boards]
                    }
                }, 200

    def post(self):
        """
        Create a board.
        """
        payload = request.get_json()
        required = ['members']
        result = validate_json(required, payload, empty=True)
        if isinstance(result, bool) is False:
            return {
                'status': 'fail',
                'message': 'Members list required.',
                'help': 'It can be empty if only oneself is a member.'
            }, 400
        else:
            members = [User.get(id=i) for i in payload['members']]
            for i in members:
                if isinstance(i, dict):
                    return {
                        'status': 'fail',
                        'message': 'The user does not exist.',
                        'missing_user': payload[
                            'members'][members.index(i)]
                    }, 404
            board = Board()
            board.insert('members', members)
            return {
                'status': 'success',
                'data': {
                    'board': board.view()
                }
            }, 201


class BoardMembersResource(Resource):
    """
    View functions for board members.
    """

    def get(self, board_id):
        """
        View members of a board.
        """
        board = Board.get(id=board_id)
        if isinstance(board, dict):
            return {
                'status': 'fail',
                'message': 'The board does not exist.',
                'help': 'Ensure board_id is of an existent board.'
            }, 404

        else:
            members = board.members
            if not members:
                return {
                    'status': 'fail',
                    'message': 'The board has no members.',
                    'help': 'Add a user to the board if necessary.'
                }, 404
            else:
                return{
                    'status': 'success',
                    'data': {
                        'members': [user.view_public() for user in board.members]

                    }
                }, 200
