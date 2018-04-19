"""
Conversation and Message manipulation functionality.
"""

from flask import request
from flask_restful import Resource


from api.helpers.auth import view_token
from api.helpers.validation import validate_json
from api.models import Conversation, Message, User


class ConversationResource(Resource):
    """
    Conversation view functions
    """

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


class MessageResource(Resource):
    """
    Message view functions.
    """

    def post(self, conversation_id):
        """
        Send a message into a conversation.
        """
        payload = request.get_json()
        required = ['content']
        result = validate_json(required, payload, empty=True)
        if isinstance(result, bool) is False:
            return {
                'status': 'fail',
                'message': 'Content required for a message.'
            }, 400
        else:
            current_user_id = current_user_id = view_token(
                request.headers.get('Authorization'))['id']
            message = Message(
                sender=current_user_id,
                content=payload['content'])
            conversation = Conversation.get(id=conversation_id)
            conversation.insert('messages', [message])
            return {
                'status': 'success',
                'data': {
                    'updated_conversation': conversation.view()
                }
            }, 201
