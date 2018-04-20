# pylint:disable=missing-docstring, invalid-name

from json import dumps, loads
from os import getenv

from api.models import Conversation, Message, User
from tests.base import BaseCase


class TestMessage(BaseCase):
    """
    Message resource tests.
    """

    def test_send_message_correctly(self):
        self.conversation1.save()
        response = self.client.post(
            '/api/v1/conversations/1/messages/',
            content_type='application/json',
            data=dumps(self.message4_dict),
            headers=self.headers)
        expected = sorted(['id', 'timestamp', 'board_id',
                           'participants', 'messages'])
        actual = sorted([i for i in loads(response.data)['data'][
            'updated_conversation']])
        self.assertEqual(201, response.status_code)
        self.assertEqual(expected, actual)

    def test_send_message_missing_content(self):
        self.conversation1.save()
        response = self.client.post(
            '/api/v1/conversations/1/messages/',
            content_type='application/json',
            data=dumps({}),
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'Content required for a message.'
        }
        actual = loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected, actual)

    def test_view_message_nonexistent_conversation(self):
        self.user1.save()
        response = self.client.get(
            '/api/v1/conversations/1/messages/',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The conversation does not exist.',
            'help': 'Ensure conversation_id is existent.'}
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, actual)

    def test_view_message(self):
        self.user1.save()
        self.conversation1.save()
        self.message1.save()
        user = User.get(id=1)
        conversation = Conversation.get(id=1)
        message = Message.get(id=1)
        conversation.insert('messages', [message])
        user.insert('conversations', [conversation])
        response = self.client.get(
            '/api/v1/conversations/1/messages/1',
            headers=self.headers)
        expected = sorted(['id', 'content', 'sender',
                           'timestamp', 'conversation_id'])
        actual = sorted([i for i in loads(response.data)['data']['message']])
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual)

    def test_view_messages(self):
        self.user1.save()
        self.conversation1.save()
        self.message1.save()
        self.message2.save()
        user = User.get(id=1)
        conversation = Conversation.get(id=1)
        messages = [Message.get(id=1), Message.get(id=2)]
        conversation.insert('messages', messages)
        user.insert('conversations', [conversation])
        response = self.client.get(
            '/api/v1/conversations/1/messages/',
            headers=self.headers)
        expected = sorted(['id', 'content', 'sender',
                           'timestamp', 'conversation_id'])
        actual1 = sorted(
            [i for i in loads(response.data)['data']['messages'][0]])
        actual2 = sorted(
            [i for i in loads(response.data)['data']['messages'][1]])
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual1)
        self.assertEqual(expected, actual2)

    def test_view_messages_none_in_conversation(self):
        self.user1.save()
        self.conversation1.save()
        user = User.get(id=1)
        conversation = Conversation.get(id=1)
        user.insert('conversations', [conversation])
        response = self.client.get(
            '/api/v1/conversations/1/messages/',
            headers=self.headers)
        expected = []
        actual = loads(response.data)['data']['messages']
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual)
