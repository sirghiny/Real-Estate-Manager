# pylint:disable=missing-docstring, invalid-name

from json import dumps, loads

from api.models import Board, Unit, User
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
            'help': 'Add boards to the database.'}
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

    def test_view_members_of_nonexistent_board(self):
        response = self.client.get(
            '/api/v1/boards/1/members/',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The board does not exist.',
            'help': 'Ensure board_id is of an existent board.'
        }
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, actual)

    def test_view_members_of_board_with_none(self):
        self.board1.save()
        response = self.client.get(
            '/api/v1/boards/1/members/',
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The board has no members.',
            'help': 'Add a user to the board if necessary.'}
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, actual)

    def test_view_members_of_board(self):
        self.board1.save()
        self.user1.save()
        self.user2.save()
        board1 = Board.get(id=1)
        board1.insert('members', *User.get_all())
        response = self.client.get(
            '/api/v1/boards/1/members/',
            headers=self.headers)
        expected = {
            'status': 'success',
            'data': {
                'members': [
                    {'id': 1, 'email': 'first1.last1@email.com',
                     'name': 'First1 Middle1 Last1',
                     'phone_number': '000 12 3456781'},
                    {'id': 2, 'email': 'first2.last2@email.com',
                     'name': 'First2 Middle2 Last2',
                     'phone_number': '000 12 3456782'}]}}
        actual = loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual)

    def test_delete_board_nonexistent(self):
        response = self.client.delete(
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

    def test_delete_board(self):
        self.board1.save()
        response = self.client.delete(
            '/api/v1/boards/1',
            headers=self.headers)
        expected = {
            'status': 'success',
            'message': 'Board with id 1 deleted.'
        }
        actual = loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual)

    def test_get_board_conversation(self):
        self.user1.save()
        self.user2.save()
        self.client.post(
            '/api/v1/boards/',
            content_type='application/json',
            data=dumps(self.board3_dict),
            headers=self.headers)
        response = self.client.get('/api/v1/boards/1/conversation/')
        expected = sorted(['id', 'timestamp', 'title',
                           'board_id', 'participants', 'messages'])
        actual = sorted(
            list(loads(response.data)['data']['conversation'].keys()))
        self.assertEqual(expected, actual)

    def test_get_board_conversation_nonexistent(self):
        response = self.client.get('/api/v1/boards/1/conversation/')
        expected = {
            'status': 'fail',
            'message': 'The board does not exist.',
            'help': 'Ensure board_id is of an existent board.'}
        actual = loads(response.data)
        self.assertEqual(expected, actual)

    def test_get_board_estate_nonexistent(self):
        response = self.client.get('/api/v1/boards/1/estates/')
        expected = {
            'status': 'fail',
            'message': 'The board does not exist.',
            'help': 'Ensure board_id is of an existent board.'}
        actual = loads(response.data)
        self.assertEqual(expected, actual)

    def test_get_board_estates(self):
        self.board1.save()
        Board.get(id=1).estates_owned.append(self.estate1)
        response = self.client.get('/api/v1/boards/1/estates/')
        expected = {
            'status': 'success',
            'data': {
                'estates': [
                    {'id': 1, 'address': 'Random Address 1', 'board_id': 1,
                     'board': {'id': 1, 'members': []},
                     'payment': 'None', 'units': []}]}}
        actual = loads(response.data)
        self.assertEqual(expected, actual)

    def test_get_board_units_nonexistent(self):
        response = self.client.get('/api/v1/boards/1/units/')
        expected = {
            'status': 'fail',
            'message': 'The board does not exist.',
            'help': 'Ensure board_id is of an existent board.'}
        actual = loads(response.data)
        self.assertEqual(expected, actual)

    def test_get_board_units(self):
        self.unit1.save()
        self.board1.save()
        unit1 = Unit.get(id=1)
        unit1.insert('estate', self.estate1)
        unit1.insert('board', self.board1)
        unit1.insert('payment', self.payment1)
        unit1.insert('resident', self.user1)
        Board.get(id=1).insert('units_owned', Unit.get(id=1))
        response = self.client.get('/api/v1/boards/1/units/')
        expected = {
            'status': 'success',
            'data': {
                'units': [
                    {'id': 1, 'name': 'Random Unit 1',
                     'board_id': 1, 'estate_id': 1, 'user_id': 1,
                     'board': {'id': 1, 'members': []},
                     'estate': {'id': 1, 'address': 'Random Address 1'},
                     'payment': {'id': 1, 'required': 0.0, 'balance': 0.0},
                     'resident': {
                         'id': 1, 'email': 'first1.last1@email.com',
                         'name': 'First1 Middle1 Last1',
                         'phone_number': '000 12 3456781'}}]}}
        actual = loads(response.data)
        self.assertEqual(expected, actual)

    def test_add_board_members(self):
        self.board1.save()
        self.user1.save()
        self.user2.save()
        board1 = Board.get(id=1)
        board1.insert('conversation', self.conversation1)
        board1.insert('members', User.get(id=1))
        response = self.client.patch(
            '/api/v1/boards/1/members/',
            headers=self.headers,
            content_type='application/json',
            data=dumps({'new_data': {'add': [2], 'remove': []}}))
        expected = {
            'status': 'success',
            'data': {
                'updated_members': [
                    {'id': 1, 'email': 'first1.last1@email.com',
                        'name': 'First1 Middle1 Last1',
                        'phone_number': '000 12 3456781'},
                    {'id': 2, 'email': 'first2.last2@email.com',
                     'name': 'First2 Middle2 Last2',
                     'phone_number': '000 12 3456782'}]}}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_remove_board_members(self):
        self.board1.save()
        self.user1.save()
        self.user2.save()
        board1 = Board.get(id=1)
        board1.insert('conversation', self.conversation1)
        board1.insert('members', User.get(id=1), User.get(id=2))
        response = self.client.patch(
            '/api/v1/boards/1/members/',
            headers=self.headers,
            content_type='application/json',
            data=dumps({'new_data': {'add': [], 'remove': [2]}}))
        expected = {
            'status': 'success',
            'data': {
                'updated_members': [
                    {'id': 1, 'email': 'first1.last1@email.com',
                        'name': 'First1 Middle1 Last1',
                        'phone_number': '000 12 3456781'}]}}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_add_and_remove_board_members(self):
        self.board1.save()
        self.user1.save()
        self.user2.save()
        board1 = Board.get(id=1)
        board1.insert('conversation', self.conversation1)
        board1.insert('members', User.get(id=1))
        response = self.client.patch(
            '/api/v1/boards/1/members/',
            headers=self.headers,
            content_type='application/json',
            data=dumps({'new_data': {'add': [2], 'remove': [1]}}))
        expected = {
            'status': 'success',
            'data': {
                'updated_members': [
                    {'id': 2, 'email': 'first2.last2@email.com',
                     'name': 'First2 Middle2 Last2',
                     'phone_number': '000 12 3456782'}]}}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_add_board_members_nonexistent(self):
        self.board1.save()
        self.user1.save()
        board1 = Board.get(id=1)
        board1.insert('conversation', self.conversation1)
        board1.insert('members', User.get(id=1))
        response = self.client.patch(
            '/api/v1/boards/1/members/',
            headers=self.headers,
            content_type='application/json',
            data=dumps({'new_data': {'add': [2], 'remove': []}}))
        expected = {
            'status': 'fail',
            'message': 'The user does not exist.',
            'help': 'Ensure ids are of existent users.'}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_remove_board_members_nonexistent(self):
        self.board1.save()
        self.user1.save()
        board1 = Board.get(id=1)
        board1.insert('conversation', self.conversation1)
        board1.insert('members', User.get(id=1))
        response = self.client.patch(
            '/api/v1/boards/1/members/',
            headers=self.headers,
            content_type='application/json',
            data=dumps({'new_data': {'add': [], 'remove': [2]}}))
        expected = {
            'status': 'fail',
            'message': 'The user is not in the board.',
            'help': 'Ensure ids are of board members.'}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_add_board_members_no_data(self):
        response = self.client.patch(
            '/api/v1/boards/1/members/',
            headers=self.headers,
            content_type='application/json',
            data=dumps({}))
        expected = {
            'status': 'fail',
            'message': 'Members list to add or remove required.',
            'help': 'Provide an id list to add or remove.'}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_add_board_members_nonexistent_board(self):
        response = self.client.patch(
            '/api/v1/boards/1/members/',
            headers=self.headers,
            content_type='application/json',
            data=dumps({'new_data': {'add': [2], 'remove': []}}))
        expected = {
            'status': 'fail',
            'message': 'The board does not exist.',
            'help': 'Ensure board_id is of an existent board.'}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)
