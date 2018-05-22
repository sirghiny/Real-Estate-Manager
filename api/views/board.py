"""
Board manipulation functionality.
"""

from flask import request
from flask_restful import Resource

from api.helpers.modelops import get_boards
from api.helpers.validation import validate_json
from api.models import Board, Conversation, User


class BoardResource(Resource):
    """
    View functions for boards.
    """

    def get(self, board_id=None):
        """
        View a board.
        """
        result = get_boards(board_id)
        if isinstance(result, dict):
            return result, 404
        elif isinstance(result, list):
            return {
                'status': 'success',
                'data': {
                    'boards': [board.view() for board in result]
                }
            }, 200
        else:
            return {
                'status': 'success',
                'data': {
                    'board': result.view()
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
            board.insert('members', *members)
            board_conversation = Conversation()
            board_conversation.participants.extend(members)
            board.insert('conversation', board_conversation)
            return {
                'status': 'success',
                'data': {
                    'board': board.view()
                }
            }, 201

    def delete(self, board_id):
        """
        Delete a board.
        """
        result = get_boards(board_id)
        if isinstance(result, dict):
            return result, 404
        else:
            result.delete()
            return {
                'status': 'success',
                'message': 'Board with id {} deleted.'.format(board_id)
            }, 200


class BoardConversationResource(Resource):
    """
    View functions for board conversations.
    """

    def get(self, board_id):
        """
        View a board's conversation.
        """
        result = get_boards(board_id)
        if isinstance(result, dict):
            return result, 404
        else:
            return {
                'status': 'success',
                'data': {
                    'conversation': result.conversation.view()
                }
            }, 200


class BoardEstatesResource(Resource):
    """
    View functions for a board's estates.
    """

    def get(self, board_id):
        """
        Get a board's estates.
        """
        result = get_boards(board_id)
        if isinstance(result, dict):
            return result, 404
        else:
            return {
                'status': 'success',
                'data': {
                    'estates': [
                        estate.view() for estate in result.estates_owned]
                }
            }, 200


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
                        'members': [
                            user.__repr__() for user in board.members]

                    }
                }, 200

    def patch(self, board_id):
        """
        Add or remove board members.
        """
        payload = request.get_json()
        required = ['new_data']
        result = validate_json(required, payload, empty=True)
        if isinstance(result, bool) is False:
            return {
                'status': 'fail',
                'message': 'Members list to add or remove required.',
                'help': 'Provide an id list to add or remove.'
            }, 400
        else:
            result = get_boards(board_id)
            if isinstance(result, dict):
                return result, 404
            else:
                if payload['new_data']['add']:
                    for i in payload['new_data']['add']:
                        i_user = User.get(id=i)
                        if isinstance(i_user, dict):
                            return {
                                'status': 'fail',
                                'message': 'The user does not exist.',
                                'help': 'Ensure ids are of existent users.'
                            }, 404
                        else:
                            result.insert('members', i_user)
                            result.conversation.insert(
                                'participants', i_user)
                if payload['new_data']['remove']:
                    members = [i.id for i in result.members]
                    for i in payload['new_data']['remove']:
                        if i not in members:
                            return {
                                'status': 'fail',
                                'message': 'The user is not in the board.',
                                'help': 'Ensure ids are of board members.'
                            }, 400
                        else:
                            result.remove('members', id=i)
                            result.conversation.remove('participants', id=i)
                updated_members = Board.get(id=board_id).members
                return {
                    'status': 'success',
                    'data': {
                        'updated_members': [
                            user.__repr__() for user in updated_members]
                    }
                }, 200


class BoardUnitsResource(Resource):
    """
    View functions for a board's units.
    """

    def get(self, board_id):
        """
        Get a board's units.
        """
        result = get_boards(board_id)
        if isinstance(result, dict):
            return result, 404
        else:
            return {
                'status': 'success',
                'data': {
                    'units': [
                        unit.view() for unit in result.units_owned]
                }
            }, 200
