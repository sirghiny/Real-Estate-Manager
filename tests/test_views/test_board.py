# pylint:disable=missing-docstring, invalid-name

from json import dumps, loads

from tests.base import BaseCase


class TestBoard(BaseCase):
    """
    Convesation resource tests.
    """

    def test_create_board_correctly(self):
        self.user1.save()
        self.user2.save()
        response = self.client.post(
            '/api/v1/boards/',
            content_type='application/json',
            data=dumps(self.board3_dict),
            headers=self.headers)
        expected = sorted(['estates_owned', 'id', 'members', 'units_owned'])
        actual = sorted([i for i in loads(response.data)['data']['board']])
        self.assertEqual(201, response.status_code)
        self.assertEqual(expected, actual)

    def test_create_board_no_members(self):
        response = self.client.post(
            '/api/v1/boards/',
            content_type='application/json',
            data=dumps({}),
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'Members list required.',
            'help': 'It can be empty if only oneself is a member.'
        }
        actual = loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected, actual)

    def test_create_board_nonexistent_members(self):
        response = self.client.post(
            '/api/v1/boards/',
            content_type='application/json',
            data=dumps(self.board3_dict),
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The user does not exist.',
            'missing_user': 1
        }
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, actual)

    def test_view_board(self):
        self.board1.save()
        response = self.client.get(
            '/api/v1/boards/1',
            headers=self.headers)
        expected = sorted(['estates_owned', 'id', 'members', 'units_owned'])
        actual = sorted([i for i in loads(response.data)['data']['board']])
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual)

    def test_view_many_boards(self):
        self.board1.save()
        self.board2.save()
        response = self.client.get(
            '/api/v1/boards/',
            headers=self.headers)
        expected = sorted(['estates_owned', 'id', 'members', 'units_owned'])
        actual1 = sorted(
            [i for i in loads(response.data)['data']['boards'][0]])
        actual2 = sorted(
            [i for i in loads(response.data)['data']['boards'][1]])
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(loads(response.data)['data']['boards']))
        self.assertEqual(expected, actual1)
        self.assertEqual(expected, actual2)

    def test_view_many_boards_if_none_exist(self):
        response = self.client.get(
            '/api/v1/boards/',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'No boards exist.',
            'help': 'Ensure there are boards in the database.'
        }
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, actual)

    def test_view_nonexistent_board(self):
        response = self.client.get(
            '/api/v1/boards/1',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The board does not exist.',
            'help': 'Ensure board_id is of an existent board.'
        }
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, actual)
