from flask import request
from flask_restful import Resource


from api.helpers.auth import view_token
from api.helpers.validation import validate_json
from api.helpers.modelops import (
    get_conversations, get_messages, update_resource)
from api.models import Conversation, Message


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
            result = get_conversations(request, conversation_id)
            if isinstance(result, dict):
                return result, 404
            else:
                current_user_id = view_token(
                    request.headers.get('Authorization'))['id']
                message = Message(
                    sender=current_user_id,
                    content=payload['content'])
                result.insert('messages', [message])
                return {
                    'status': 'success',
                    'data': {
                        'updated_conversation': result.view()
                    }
                }, 201

    def get(self, conversation_id, message_id=None):
        """
        View message(s).
        """
        result = get_messages(request, conversation_id, message_id)
        if isinstance(result, dict):
            return result, 404
        elif isinstance(result, list):
            return {
                'status': 'success',
                'data': {
                    'messages': [
                        message.view() for message in result
                    ]
                }
            }, 200
        else:
            return {
                'status': 'success',
                'data': {
                    'message': result.view()
                }
            }, 200

    def delete(self, conversation_id, message_id):
        """
        Delete message.
        """
        result = get_messages(request, conversation_id, message_id)
        if isinstance(result, dict):
            return result, 404
        else:
            result.delete()
            updated_conversation = Conversation.get(id=conversation_id).view()
            return {
                'status': 'success',
                'data': {
                    'updated_conversation': updated_conversation
                }
            }, 200

    def patch(self, conversation_id, message_id):
        """
        Edit a message.
        """
        result = get_messages(request, conversation_id, message_id)
        if isinstance(result, dict):
            return result, 404
        else:
            update_result = update_resource(request, result)
            if isinstance(update_result, bool):
                updated_conversation = Conversation.get(
                    id=conversation_id).view()
                return {
                    'status': 'success',
                    'data': {
                        'updated_conversation': updated_conversation
                    }
                }, 200
            else:
                return update_result, 400
