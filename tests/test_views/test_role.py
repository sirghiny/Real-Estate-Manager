# pylint:disable=missing-docstring, invalid-name

from json import loads

from api.models import Role, User
from tests.base import BaseCase


class TestRole(BaseCase):
    """
    Role resource tests.
    """

    def test_get_roles_none_in_db(self):
        response = self.client.get(
            '/api/v1/roles/',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'There are no roles in the system.',
            'help': 'Ensure roles are seeded.'}
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, actual)

    def test_get_role(self):
        self.role1.save()
        response = self.client.get(
            '/api/v1/roles/1',
            headers=self.headers)
        expected = {
            'status': 'success',
            'data': {
                'role': {'id': 1, 'title': 'basic'}}}
        actual = loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual)

    def test_get_nonexistent_role(self):
        response = self.client.get(
            '/api/v1/roles/1',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The role does not exist.',
            'help': 'Ensure role_id is existent.'}
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, actual)

    def test_get_roles(self):
        self.role1.save()
        self.role2.save()
        response = self.client.get(
            '/api/v1/roles/',
            headers=self.headers)
        expected = {
            'status': 'success',
            'data': {
                'roles': [
                    {'id': 1, 'title': 'basic'}, {'id': 2, 'title': 'admin'}]}}
        actual = loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual)

    def test_get_role_users_nonexistent_role(self):
        response = self.client.get(
            '/api/v1/roles/1/users/',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The role does not exist.',
            'help': 'Ensure role_id is existent.'}
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_get_role_users_when_none_added(self):
        self.role1.save()
        response = self.client.get(
            '/api/v1/roles/1/users/',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The role has no users.',
            'help': 'Have an admin add users to the role.'}
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected, actual)

    def test_get_role_users(self):
        self.role1.save()
        self.user1.save()
        self.user2.save()
        role1 = Role.get(id=1)
        role1.insert('users', *User.get_all())
        response = self.client.get('/api/v1/roles/1/users/',
                                   headers=self.headers)
        expected = {
            'status': 'success',
            'data': {
                'role': {'id': 1,
                         'title': 'basic',
                         'users': [
                             {'id': 1, 'email': 'first1.last1@email.com',
                              'name': 'First1 Middle1 Last1',
                              'phone_number': '000 12 3456781'},
                             {'id': 2, 'email': 'first2.last2@email.com',
                              'name': 'First2 Middle2 Last2',
                              'phone_number': '000 12 3456782'}]}}}
        actual = loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(expected, actual)
