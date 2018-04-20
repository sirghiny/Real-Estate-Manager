# pylint:disable=missing-docstring, invalid-name

from json import dumps, loads
from os import getenv

from api.models import Board, Role, User, Wallet
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
            'message': 'Not all fields were provided.',
            'missing': 'email, name, password, phone_number'
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
            'help': 'Ensure arguments are of existent object.'
        }
        self.assertDictEqual(expected, loads(response.data))
        self.assertEqual(404, response.status_code)

    def test_search_user_single_result(self):
        self.user1.save()
        self.user2.save()
        response = self.client.get(
            '/api/v1/users/?q=First1', headers=self.headers)
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
            '/api/v1/users/?q=First', headers=self.headers)
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
            '/api/v1/users/?q=Random', headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'No users with the name in the database.'}
        self.assertDictEqual(expected, loads(response.data))
        self.assertEqual(404, response.status_code)

    def test_view_user_boards_nonexistent_user(self):
        response = self.client.get(
            '/api/v1/users/1/boards/',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The user does not exist.',
            'help': 'Ensure arguments are of existent object.'
        }
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_view_user_boards_user_has_none(self):
        self.user1.save()
        response = self.client.get(
            '/api/v1/users/1/boards/',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The user is not in any boards.',
            'help': 'Suggest a board if necessary.'
        }
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_view_user_boards(self):
        self.user1.save()
        self.board1.save()
        user1 = User.get(id=1)
        user1.insert('boards', [Board.get(id=1)])
        response = self.client.get(
            '/api/v1/users/1/boards/',
            headers=self.headers)
        expected = {
            'status': 'success',
            'data': {
                'boards': [
                    {'id': 1, 'members': [
                        {'id': 1, 'email': 'first1.last1@email.com',
                         'name': 'First1 Middle1 Last1',
                         'phone_number': '000 12 3456781'}],
                        'estates_owned': [], 'units_owned': []}]}}
        actual = loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_view_users_roles_nonexistent_user(self):
        response = self.client.get(
            '/api/v1/users/1/roles/',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The user does not exist.',
            'help': 'Ensure arguments are of existent objects and unique.'
        }
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_view_users_roles(self):
        self.user1.save()
        self.role1.save()
        user1 = User.get(id=1)
        user1.insert('roles', Role.get_all())
        response = self.client.get(
            '/api/v1/users/1/roles/',
            headers=self.headers)
        expected = {
            'status': 'success',
            'data': {
                'roles': [
                    {'id': 1, 'title': 'basic'}]}}
        actual = loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_view_wallet_nonexistent_user(self):
        response = self.client.get(
            '/api/v1/users/1/wallet/',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The user does not exist.',
            'help': 'Ensure arguments are of existent objects and unique.'
        }
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_view_user_wallet(self):
        self.user1.save()
        self.wallet1.save()
        user1 = User.get(id=1)
        user1.insert('wallet', Wallet.get(id=1))
        response = self.client.get(
            '/api/v1/users/1/wallet/',
            headers=self.headers)
        expected = {
            'status': 'success',
            'data': {
                'wallet': {
                    'id': 1, 'balance': 0.0, 'user_id': 1, 'payments': []}}}
        actual = loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(expected, actual)
