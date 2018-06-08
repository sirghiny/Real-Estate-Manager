"""Conversation and Message manipulation functionality."""

from flask import request
from flask_restful import Resource


from api.helpers.auth import token_required, view_token
from api.helpers.modelops import get_conversations
from api.helpers.validation import validate_json
from api.models import Conversation, User


class ConversationResource(Resource):
    """Conversation view functions."""

    @token_required
    def post(self):
        """Create a conversation."""
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
            conversation.insert('participants', *participants)
            return {
                'status': 'success',
                'data': {'conversation': conversation.view()}
            }, 201

    @token_required
    def get(self, conversation_id=None):
        """Get a user's conversation(s)."""
        result = get_conversations(request, conversation_id)
        if isinstance(result, dict):
            return result, 404
        elif isinstance(result, list):
            return {
                'status': 'success',
                'data': {'conversations': [i.view() for i in result]}
            }, 200
        else:
            return {
                'status': 'success',
                'data': {'conversation': result.view()}
            }, 200

    def delete(self, conversation_id):
        """
        Delete a conversation.

        Remove user, only delete if last member deletes.
        """
        result = get_conversations(request, conversation_id)
        if isinstance(result, dict):
            return result, 404
        else:
            no_participants = len(result.participants)
            if no_participants == 1:
                result.delete()
            else:
                user = User.get(email=view_token(
                    request.headers.get('Authorization'))['email'])
                user.remove('conversations', id=conversation_id)
            return {
                'status': 'success',
                'message': 'The conversation has been deleted.'
            }, 200
