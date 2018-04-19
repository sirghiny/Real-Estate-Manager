# pylint:disable=missing-docstring, invalid-name

from json import dumps, loads
from os import getenv

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
