from flask import request
from flask_restful import Resource


from api.helpers.auth import view_token
from api.helpers.validation import validate_json
from api.models import Conversation, Message, User


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

    def get(self, conversation_id, message_id=None):
        """
        View message(s).
        """
        user = User.get(email=view_token(
            request.headers.get('Authorization'))['email'])
        conversations = user.conversations
        try:
            conversation = [conversation for conversation in conversations
                            if conversation.id == conversation_id][0]
            if message_id:
                try:
                    message = [
                        message for message in conversation.messages][0]
                    return {
                        'status': 'success',
                        'data': {
                            'message': message.view()
                        }
                    }, 200
                except IndexError:
                    return {
                        'status': 'fail',
                        'message': 'The message does not exist.',
                        'help': 'Ensure message_id is existent.'
                    }, 404
            else:
                return {
                    'status': 'success',
                    'data': {
                        'messages': [
                            message.view() for message in conversation.messages
                        ]
                    }
                }, 200
        except IndexError:
            return {
                'status': 'fail',
                'message': 'The conversation does not exist.',
                'help': 'Ensure conversation_id is existent.'
            }, 404
