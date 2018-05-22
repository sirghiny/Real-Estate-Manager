# pylint:disable=missing-docstring, invalid-name

from json import dumps, loads

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

    def test_get_user_bad_token(self):
        self.user1.save()
        response1 = self.client.get(
            '/api/v1/users/1', headers=self.bad_headers1)
        response2 = self.client.get(
            '/api/v1/users/1', headers=self.bad_headers2)
        expected1 = {
            'status': 'fail',
            'error': 'Bad request',
            'message': 'Signature verification failed'}
        expected2 = {
            'status': 'fail',
            'error': 'Bad request',
            'message': 'Expired token.'}
        actual1 = loads(response1.data)
        actual2 = loads(response2.data)
        self.assertEqual(expected1, actual1)
        self.assertEqual(expected2, actual2)

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
            '/api/v1/users/all/', headers=self.headers)
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
            '/api/v1/users/all/', headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'There are no users in the database.',
            'help': 'Ensure there are some users in the database'}
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
            'message': 'No users with the name in the database.',
            'help': 'Try searching with another name.'}
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
        user1.insert('boards', Board.get(id=1))
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
            'help': 'Ensure arguments are of existent object.'}
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_view_users_roles(self):
        self.user1.save()
        self.role1.save()
        user1 = User.get(id=1)
        user1.insert('roles', *Role.get_all())
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
            '/api/v1/users/wallet/',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The user does not exist.',
            'help': 'Ensure arguments are of existent object.'}
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_view_user_wallet(self):
        self.user1.save()
        self.wallet1.save()
        user1 = User.get(id=1)
        user1.insert('wallet', Wallet.get(id=1))
        response = self.client.get(
            '/api/v1/users/wallet/',
            headers=self.headers)
        expected = {
            'status': 'success',
            'data': {
                'wallet': {
                    'id': 1, 'balance': 0.0, 'user_id': 1, 'payments': []}}}
        actual = loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_update_user(self):
        self.user1.save()
        response = self.client.patch('/api/v1/users/',
                                     content_type='application/json',
                                     data=dumps(
                                         {'new_data': {'name': 'New Name'}}),
                                     headers=self.headers)
        self.assertEqual('New Name',
                         (loads(response.data))['data']['user']['name'])

    def test_update_user_wrong_attribute(self):
        self.user1.save()
        response = self.client.patch('/api/v1/users/',
                                     content_type='application/json',
                                     data=dumps(
                                         {'new_data': {'random': 'Random'}}),
                                     headers=self.headers)
        self.assertEqual(400, response.status_code)
        expected = {
            'message': 'Error encountered when setting attributes.',
            'help': "Ensure all fields you're updating are valid."}
        actual = loads(response.data)
        self.assertEqual(expected, actual)

    def test_update_user_no_data(self):
        self.user1.save()
        response = self.client.patch('/api/v1/users/',
                                     content_type='application/json',
                                     data=dumps(
                                         {}),
                                     headers=self.headers)
        self.assertEqual(400, response.status_code)
        expected = {
            'status': 'fail',
            'message': 'Not all fields were provided.',
            'missing': 'new_data'
        }
        actual = loads(response.data)
        self.assertEqual(expected, actual)

    def test_update_user_nonexistent(self):
        response = self.client.patch('/api/v1/users/',
                                     content_type='application/json',
                                     data=dumps(
                                         {'new_data': {'name': 'New Name'}}),
                                     headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The user does not exist.',
            'help': 'Ensure arguments are of existent object.'}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_delete_user_nonexistent(self):
        response = self.client.delete('/api/v1/users/',
                                      headers=self.headers)
        self.assertEqual(404, response.status_code)
        expected = {
            'status': 'fail',
            'message': 'The user does not exist.',
            'help': 'Ensure arguments are of existent object.'}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_delete_user(self):
        self.user1.save()
        response = self.client.delete('/api/v1/users/',
                                      headers=self.headers)
        self.assertEqual(200, response.status_code)
        expected = {
            'status': 'success',
            'message': 'User with id 1 has been deleted.'}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)
        self.assertTrue(isinstance(User.get_all(), dict))
