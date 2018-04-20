# pylint:disable=missing-docstring, invalid-name

from json import dumps, loads

from tests.base import BaseCase


class TestAuth(BaseCase):
    """
    Authorization resource tests.
    """

    def test_login_nonexistent_user(self):
        response = self.client.post(
            '/api/v1/signin/',
            data=dumps({'email': 'nonexistent',
                        'password': 'nonexistent'}),
            content_type='application/json',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The user does not exist.',
            'help': 'Ensure arguments are of existent object.'
        }
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_sign_in_user_no_email(self):
        response = self.client.post(
            '/api/v1/signin/',
            content_type='application/json',
            data=dumps({'password': 'password123'}))
        expected = {
            'status': 'fail',
            'message': 'Not all fields were provided.',
            'missing': 'email'
        }
        self.assertDictEqual(expected, loads(response.data))
        self.assertEqual(400, response.status_code)

    def test_sign_in_wrong_password(self):
        self.user1.save()
        response = self.client.post(
            '/api/v1/signin/',
            content_type='application/json',
            data=dumps({'email': 'first1.last1@email.com',
                        'password': 'password123'}))
        expected = {
            'status': 'fail',
            'message': 'Wrong password.',
            'help': 'Recover the password if necessary.'
        }
        self.assertDictEqual(expected, loads(response.data))
        self.assertEqual(400, response.status_code)

    def test_sign_in_correctly(self):
        self.user1.save()
        response = self.client.post(
            '/api/v1/signin/',
            content_type='application/json',
            data=dumps({'email': 'first1.last1@email.com',
                        'password': 'ABC123!@#'}))
        expected = 'Welcome to Real Estate Manager.'
        self.assertEqual(expected, loads(response.data)['data']['message'])
        self.assertEqual(200, response.status_code)
