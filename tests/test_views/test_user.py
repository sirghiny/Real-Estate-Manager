# pylint:disable=missing-docstring, invalid-name

from json import dumps, loads
from os import getenv

from tests.base import BaseCase


class TestUser(BaseCase):
    """
    User resource tests.
    """

    def test_create_user_correctly(self):
        self.role1.save()
        response = self.client.post(
            '/api/v1/users/',
            content_type='application/json',
            data=dumps(self.user1_dict))
        expected = {
            'status': 'success',
            'message': 'User with id 1 was created.'
        }
        self.assertDictEqual(expected, loads(response.data))
        self.assertEqual(201, response.status_code)

    def test_create_user_missing_data(self):
        response = self.client.post(
            '/api/v1/users/', content_type='application/json', data=dumps({}))
        expected = {
            'status': 'fail',
            'data': {
                'missing': 'email, name, password, phone_number'}
        }
        self.assertDictEqual(expected, loads(response.data))
        self.assertEqual(400, response.status_code)

    def test_get_user_correctly(self):
        self.user1.save()
        response = self.client.get(
            '/api/v1/users/1', headers=self.headers)
        expected = {
            'status': 'success',
            'data': {
                'id': 1,
                'email': 'first1.last1@email.com',
                'name': 'First1 Middle1 Last1',
                'phone_number': '000 12 3456781'}}
        self.assertDictEqual(expected, loads(response.data))
        self.assertEqual(200, response.status_code)

    def test_get_users_no_authorization(self):
        response = self.client.get(
            '/api/v1/users/')
        self.assertEqual(400, response.status_code)
        expected = {
            "status": "fail",
            "error": "Bad request",
            "message": "Header does not contain authorization token."
        }
        self.assertEqual(expected, loads(response.data))

    def test_get_users(self):
        self.user1.save()
        self.user2.save()
        response = self.client.get(
            '/api/v1/users/', headers=self.headers)
        expected = {
            'status': 'success',
            'data': {
                'users': [
                    {'id': 1,
                     'email': 'first1.last1@email.com',
                     'name': 'First1 Middle1 Last1',
                     'phone_number': '000 12 3456781'},
                    {'id': 2,
                     'email': 'first2.last2@email.com',
                     'name': 'First2 Middle2 Last2',
                     'phone_number': '000 12 3456782'}]}}
        self.assertDictEqual(expected, loads(response.data))
        self.assertEqual(200, response.status_code)

    def test_get_users_when_none_is_in_database(self):
        response = self.client.get(
            '/api/v1/users/', headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'No users in the database.'
        }
        self.assertDictEqual(expected, loads(response.data))
        self.assertEqual(404, response.status_code)

    def test_get_user_who_does_not_exist(self):
        response = self.client.get(
            '/api/v1/users/1', headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The user does not exist.',
            'help': 'Ensure arguments are of existent objects and unique.'
        }
        self.assertDictEqual(expected, loads(response.data))
        self.assertEqual(404, response.status_code)

    def test_search_user_single_result(self):
        self.user1.save()
        self.user2.save()
        response = self.client.get(
            '/api/v1/users/?name=First1', headers=self.headers)
        expected = {
            'status': 'success',
            'data': {
                'users': [
                    {'id': 1,
                     'email': 'first1.last1@email.com',
                     'name': 'First1 Middle1 Last1',
                     'phone_number': '000 12 3456781'}]}}
        self.assertDictEqual(expected, loads(response.data))
        self.assertEqual(200, response.status_code)

    def test_search_user_several_results(self):
        self.user1.save()
        self.user2.save()
        response = self.client.get(
            '/api/v1/users/?name=First', headers=self.headers)
        expected = {
            'status': 'success',
            'data': {
                'users': [
                    {'id': 1,
                     'email': 'first1.last1@email.com',
                     'name': 'First1 Middle1 Last1',
                     'phone_number': '000 12 3456781'},
                    {'id': 2,
                     'email': 'first2.last2@email.com',
                     'name': 'First2 Middle2 Last2',
                     'phone_number': '000 12 3456782'}]}}
        self.assertDictEqual(expected, loads(response.data))
        self.assertEqual(200, response.status_code)

    def test_search_user_no_result(self):
        self.user1.save()
        self.user2.save()
        response = self.client.get(
            '/api/v1/users/?name=Random', headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'No users with the name in the database.'}
        self.assertDictEqual(expected, loads(response.data))
        self.assertEqual(404, response.status_code)

    def test_sign_in_user_no_email(self):
        response = self.client.post(
            '/api/v1/signin/',
            content_type='application/json',
            data=dumps({'password': 'password123'}))
        expected = {
            'status': 'fail',
            'data': {'missing': 'email'}
        }
        self.assertDictEqual(expected, loads(response.data))
        self.assertEqual(400, response.status_code)

    def test_sign_in_user_not_in_database(self):
        response = self.client.post(
            '/api/v1/signin/',
            content_type='application/json',
            data=dumps({'email': 'random@email.com',
                        'password': 'password123'}))
        expected = {
            'status': 'fail',
            'data': {'message': 'User does not exist.'}
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
            'data': {'message': 'Wrong password.'}
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
        expected = 'Welcome to Real Estate Manager!'
        self.assertEqual(expected, loads(response.data)['data']['message'])
        self.assertEqual(200, response.status_code)
