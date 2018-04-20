"""
Conversation and Message manipulation functionality.
"""

from flask import request
from flask_restful import Resource


from api.helpers.auth import token_required, view_token
from api.helpers.validation import validate_json
from api.models import Conversation, User


class ConversationResource(Resource):
    """
    Conversation view functions
    """

    @token_required
    def post(self):
        """
        Create a conversation.
        """
        payload = request.get_json()
        required = ['participants']
        result = validate_json(required, payload, empty=True)
        if isinstance(result, bool) is False:
            return {
                'status': 'fail',
                'message': 'Participants list required.',
                'help': 'It can be empty if conversing with oneself.'
            }, 400
        else:
            current_user_id = view_token(
                request.headers.get('Authorization'))['id']
            if current_user_id not in payload['participants']:
                payload['participants'].append(current_user_id)
            participants = [User.get(id=i) for i in payload['participants']]
            for i in participants:
                if isinstance(i, dict):
                    return {
                        'status': 'fail',
                        'message': 'The user does not exist.',
                        'missing_user': payload[
                            'participants'][participants.index(i)]
                    }, 404
            conversation = Conversation()
            conversation.insert('participants', participants)
            return {
                'status': 'success',
                'data': {
                    'conversation': conversation.view()
                }
            }, 201

    @token_required
    def get(self, conversation_id=None):
        """
        Get a user's conversation(s).
        """
        user = User.get(email=view_token(
            request.headers.get('Authorization'))['email'])
        conversations = user.conversations
        if conversation_id:
            conversation = [conversation for conversation in conversations
                            if conversation.id == conversation_id]
            if conversation:
                return {
                    'status': 'success',
                    'data': {
                        'conversation': conversation[0].view()
                    }
                }, 200
            return {
                'status': 'fail',
                'message': 'The conversation does not exist.',
                'help': 'Ensure conversation_id is existent.'
            }, 404
        if conversations:
            return {
                'status': 'success',
                'data': {
                    'conversations': [
                        conversation.view() for conversation in conversations]
                }
            }, 200
        return {
            'status': 'fail',
            'message': 'The user has no conversations.',
            'help': 'Open at least one conversation.'
        }, 404
