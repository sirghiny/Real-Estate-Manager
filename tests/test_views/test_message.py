# pylint:disable=missing-docstring, invalid-name

from json import dumps, loads

from api.models import Conversation, User
from tests.base import BaseCase


class TestMessage(BaseCase):
    """
    Message resource tests.
    """

    def test_send_message_correctly(self):
        self.user1.save()
        User.get(id=1).insert('conversations', [self.conversation1])
        response = self.client.post(
            '/api/v1/conversations/1/messages/',
            content_type='application/json',
            data=dumps(self.message4_dict),
            headers=self.headers)
        expected = sorted(['id', 'timestamp', 'board_id',
                           'participants', 'messages', 'title'])
        actual = sorted([i for i in loads(response.data)['data'][
            'updated_conversation']])
        self.assertEqual(201, response.status_code)
        self.assertEqual(expected, actual)

    def test_send_message_missing_content(self):
        self.user1.save()
        User.get(id=1).insert('conversations', [self.conversation1])
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

    def test_send_message_nonexistent_conversation(self):
        self.user1.save()
        response = self.client.post(
            '/api/v1/conversations/1/messages/',
            content_type='application/json',
            data=dumps(self.message4_dict),
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The user has no conversations.',
            'help': 'Open at least one conversation.'}
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, actual)

    def test_view_message_nonexistent_conversation(self):
        self.user1.save()
        User.get(id=1).insert('conversations', [self.conversation1])
        response = self.client.get(
            '/api/v1/conversations/2/messages/',
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
        User.get(id=1).insert('conversations', [self.conversation1])
        Conversation.get(id=1).insert('messages', [self.message1])
        response = self.client.get(
            '/api/v1/conversations/1/messages/1',
            headers=self.headers)
        expected = sorted(['id', 'content', 'edited', 'sender',
                           'timestamp', 'conversation_id'])
        actual = sorted([i for i in loads(response.data)['data']['message']])
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual)

    def test_view_nonexistent_message_in_conversation(self):
        self.user1.save()
        User.get(id=1).insert('conversations', [self.conversation1])
        response = self.client.get(
            '/api/v1/conversations/1/messages/1',
            headers=self.headers)
        self.assertEqual(404, response.status_code)
        expected = {
            'status': 'fail',
            'message': 'The message does not exist.',
            'help': 'Ensure message_id is existent.'}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_view_messages(self):
        self.user1.save()
        User.get(id=1).insert('conversations', [self.conversation1])
        Conversation.get(id=1).insert(
            'messages', [self.message1, self.message2])
        response = self.client.get(
            '/api/v1/conversations/1/messages/',
            headers=self.headers)
        expected = sorted(['id', 'content', 'edited', 'sender',
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
        expected = {
            'status': 'fail',
            'message': 'The conversation has no messages.',
            'help': 'Send at least one message.'}
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, actual)

    def test_delete_message_nonexistent_conversation(self):
        self.user1.save()
        response = self.client.delete(
            '/api/v1/conversations/1/messages/1',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The user has no conversations.',
            'help': 'Open at least one conversation.'}
        actual = loads(response.data)
        self.assertEqual(expected, actual)

    def test_delete_nonexistent_message(self):
        self.user1.save()
        User.get(id=1).insert('conversations', [self.conversation1])
        response = self.client.delete(
            '/api/v1/conversations/1/messages/1',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The message does not exist.',
            'help': 'Ensure message_id is existent.'}
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, actual)

    def test_delete_message(self):
        self.user1.save()
        User.get(id=1).insert('conversations', [self.conversation1])
        Conversation.get(id=1).insert('messages', [self.message1])
        response = self.client.delete(
            '/api/v1/conversations/1/messages/1',
            headers=self.headers)
        expected = []
        actual = loads(response.data)['data'][
            'updated_conversation']['messages']
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual)

    def test_update_message(self):
        self.user1.save()
        User.get(id=1).insert('conversations', [self.conversation1])
        Conversation.get(id=1).insert('messages', [self.message1])
        response = self.client.patch(
            '/api/v1/conversations/1/messages/1',
            headers=self.headers,
            content_type='application/json',
            data=dumps({'new_data': {'content': 'New Content'}}))
        expected = 'New Content'
        actual = loads(response.data)['data'][
            'updated_conversation']['messages'][0]['content']
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual)

    def test_update_message_nonexistent_conversation(self):
        self.user1.save()
        response = self.client.patch(
            '/api/v1/conversations/1/messages/1',
            headers=self.headers,
            content_type='application/json',
            data=dumps({'new_data': {'content': 'New Content'}}))
        expected = {
            'status': 'fail',
            'message': 'The user has no conversations.',
            'help': 'Open at least one conversation.'
        }
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_update_message_no_data(self):
        self.user1.save()
        User.get(id=1).insert('conversations', [self.conversation1])
        Conversation.get(id=1).insert('messages', [self.message1])
        response = self.client.patch(
            '/api/v1/conversations/1/messages/1',
            headers=self.headers,
            content_type='application/json',
            data=dumps({}))
        expected = {
            'status': 'fail',
            'message': 'Not all fields were provided.',
            'missing': 'new_data'}
        actual = loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected, actual)
