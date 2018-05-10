# pylint:disable=missing-docstring, invalid-name

from json import dumps, loads

from api.models import Conversation, User
from tests.base import BaseCase


class TestConversation(BaseCase):
    """
    Convesation resource tests.
    """

    def test_create_conversation_correctly(self):
        self.user1.save()
        self.user2.save()
        response = self.client.post(
            '/api/v1/conversations/',
            content_type='application/json',
            data=dumps(self.conversation3_dict),
            headers=self.headers)
        expected = sorted(['participants', 'messages',
                           'board_id', 'id', 'timestamp', 'title'])
        actual = sorted(
            [i for i in loads(response.data)['data']['conversation']])
        self.assertEqual(201, response.status_code)
        self.assertEqual(expected, actual)

    def test_create_conversation_creator_ommited(self):
        self.user1.save()
        self.user2.save()
        response = self.client.post(
            '/api/v1/conversations/',
            content_type='application/json',
            data=dumps(self.conversation4_dict),
            headers=self.headers)
        expected = sorted(['participants', 'messages',
                           'board_id', 'id', 'timestamp', 'title'])
        actual = sorted(
            [i for i in loads(response.data)['data']['conversation']])
        self.assertEqual(201, response.status_code)
        self.assertEqual(expected, actual)

    def test_create_conversation_no_participants(self):
        self.user1.save()
        self.user2.save()
        response = self.client.post(
            '/api/v1/conversations/',
            content_type='application/json',
            data=dumps({}),
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'Participants list required.',
            'help': 'It can be empty if conversing with oneself.'
        }
        actual = loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected, actual)

    def test_create_conversation_nonexistent_participant(self):
        self.user1.save()
        response = self.client.post(
            '/api/v1/conversations/',
            content_type='application/json',
            data=dumps(self.conversation3_dict),
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The user does not exist.',
            'missing_user': 2
        }
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, actual)

    def test_get_conversation_when_none_exist(self):
        self.user1.save()
        response = self.client.get(
            '/api/v1/conversations/1',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The user has no conversations.',
            'help': 'Open at least one conversation.'}
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_get_conversations_when_none_exist(self):
        self.user1.save()
        response = self.client.get(
            '/api/v1/conversations/',
            headers=self.headers)
        expected = {
            'status': 'fail', 'message': 'The user has no conversations.',
            'help': 'Open at least one conversation.'}
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_get_conversation(self):
        self.user1.save()
        self.conversation1.save()
        user1 = User.get(id=1)
        user1.insert('conversations', [Conversation.get(id=1)])
        response = self.client.get(
            '/api/v1/conversations/1',
            headers=self.headers)
        expected = sorted(['id', 'timestamp', 'board_id',
                           'participants', 'messages', 'title'])
        actual = sorted([i for i in loads(response.data)
                         ['data']['conversation']])
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual)

    def test_get_conversations(self):
        self.user1.save()
        self.conversation1.save()
        self.conversation2.save()
        user1 = User.get(id=1)
        user1.insert('conversations', [
                     Conversation.get(id=1), Conversation.get(id=2)])
        response = self.client.get(
            '/api/v1/conversations/',
            headers=self.headers)
        expected = sorted(['id', 'timestamp', 'board_id',
                           'participants', 'messages', 'title'])
        actual1 = sorted([i for i in loads(response.data)
                          ['data']['conversations'][0]])
        actual2 = sorted([i for i in loads(response.data)
                          ['data']['conversations'][1]])
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual1)
        self.assertEqual(expected, actual2)

    def test_delete_conversations_when_none_exist(self):
        self.user1.save()
        response = self.client.delete(
            '/api/v1/conversations/1/',
            headers=self.headers)
        self.assertEqual(404, response.status_code)
        expected = {
            'status': 'fail',
            'message': 'The user has no conversations.',
            'help': 'Open at least one conversation.'
        }
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_delete_conversations_when_specific_does_not_exist(self):
        self.user1.save()
        User.get(id=1).insert('conversations', [self.conversation1])
        response = self.client.delete(
            '/api/v1/conversations/2/',
            headers=self.headers)
        self.assertEqual(404, response.status_code)
        expected = {
            'status': 'fail',
            'message': 'The conversation does not exist.',
            'help': 'Ensure conversation_id is existent.'
        }
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_delete_conversations_when_only_one_participant_is_left(self):
        self.user1.save()
        User.get(id=1).insert('conversations', [self.conversation1])
        response = self.client.delete(
            '/api/v1/conversations/1/',
            headers=self.headers)
        self.assertEqual(200, response.status_code)
        expected = {
            'status': 'success',
            'message': 'The conversation has been deleted.'
        }
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)
        conversation = Conversation.get(id=1)
        self.assertTrue(isinstance(conversation, dict))

    def test_delete_conversations_when_only_participants_are_left(self):
        self.conversation1.save()
        Conversation.get(id=1).insert('participants', [self.user1, self.user2])
        response = self.client.delete(
            '/api/v1/conversations/1/',
            headers=self.headers)
        self.assertEqual(200, response.status_code)
        expected = {
            'status': 'success',
            'message': 'The conversation has been deleted.'
        }
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)
        conversation = Conversation.get(id=1)
        self.assertTrue(isinstance(conversation, Conversation))
