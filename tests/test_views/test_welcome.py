# pylint:disable=missing-docstring, invalid-name

from json import loads

from tests.base import BaseCase


class TestWelcome(BaseCase):
    """
    Welcome resource tests.
    """

    def test_welcome(self):
        response = self.client.get('/')
        expected = {
            'status': 'success',
            'data': {
                'message': 'Welcome to Real Estate Manager.'
            }
        }
        self.assertEqual(expected, loads(response.data))
        self.assertEqual(200, response.status_code)
