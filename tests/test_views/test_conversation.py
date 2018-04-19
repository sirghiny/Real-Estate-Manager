# pylint:disable=missing-docstring, invalid-name

from json import dumps, loads
from os import getenv

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
                           'board_id', 'id', 'timestamp'])
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
