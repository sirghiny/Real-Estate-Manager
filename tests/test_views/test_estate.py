# pylint:disable=missing-docstring, invalid-name

from json import dumps, loads

from api.models import Board, Estate, Payment
from tests.base import BaseCase


class TestEstate(BaseCase):
    """
    Estate resource tests.
    """

    def test_view_estate_nonexistent(self):
        response = self.client.get(
            '/api/v1/estates/1'
        )
        self.assertEqual(404, response.status_code)
        expected = {
            'status': 'fail',
            'message': 'The estate does not exist.',
            'help': 'Ensure estate_id is of an existent estate.'
        }
        actual = loads(response.data)
        self.assertEqual(expected, actual)

    def test_view_estate(self):
        self.estate1.save()
        self.board1.save()
        self.payment1.save()
        estate1 = Estate.get(id=1)
        estate1.insert('payment', Payment.get(id=1))
        estate1.insert('board', Board.get(id=1))
        response = self.client.get(
            '/api/v1/estates/1'
        )
        self.assertEqual(200, response.status_code)
        expected = {
            'status': 'success',
            'data': {
                'estate': {
                    'id': 1, 'address': 'Random Address 1', 'board_id': 1,
                    'board': {'id': 1, 'members': []},
                    'payment': {'id': 1, 'required': 0.0, 'balance': 0.0},
                    'units': []}}}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_view_estates_nonexistent(self):
        response = self.client.get(
            '/api/v1/estates/'
        )
        self.assertEqual(404, response.status_code)
        expected = {
            'status': 'fail',
            'message': 'No estates exist.',
            'help': 'Add estates to the database.'}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_view_estates(self):
        self.estate1.save()
        self.board1.save()
        self.payment1.save()
        estate1 = Estate.get(id=1)
        estate1.insert('payment', Payment.get(id=1))
        estate1.insert('board', Board.get(id=1))
        response = self.client.get(
            '/api/v1/estates/'
        )
        self.assertEqual(200, response.status_code)
        expected = {
            'status': 'success',
            'data': {
                'estates': [
                    {'id': 1, 'address': 'Random Address 1', 'board_id': 1,
                     'board': {'id': 1, 'members': []},
                     'payment': {
                         'id': 1, 'required': 0.0, 'balance': 0.0},
                        'units': []}]}}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_view_estate_payment_nonexistent(self):
        response = self.client.get(
            '/api/v1/estates/1/payment/'
        )
        self.assertEqual(404, response.status_code)
        expected = {
            'status': 'fail',
            'message': 'The estate does not exist.',
            'help': 'Ensure estate_id is of an existent estate.'}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_view_estate_payment(self):
        self.estate1.save()
        self.payment1.save()
        estate1 = Estate.get(id=1)
        estate1.insert('payment', Payment.get(id=1))
        response = self.client.get(
            '/api/v1/estates/1/payment/'
        )
        self.assertEqual(200, response.status_code)
        expected = {
            'status': 'success',
            'data': {
                'payment': {
                    'id': 1, 'balance': 0.0, 'required': 0.0, 'estate_id': 1,
                    'unit_id': None, 'wallet_id': None, 'deposits': []}}}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)

    def test_create_estate(self):
        self.board1.save()
        response = self.client.post(
            '/api/v1/estates/',
            content_type='application/json',
            data=dumps(self.estate4_dict),
            headers=self.headers)
        expected = {
            'status': 'success',
            'message': 'Estate with id 1 created.'}
        actual = loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(expected, actual)

    def test_create_estate_nonexistent_board(self):
        response = self.client.post(
            '/api/v1/estates/',
            content_type='application/json',
            data=dumps(self.estate4_dict),
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'The board does not exist.',
            'help': 'Ensure board_id is of an existent board.'}
        actual = loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, actual)

    def test_create_estate_no_data(self):
        response = self.client.post(
            '/api/v1/estates/',
            content_type='application/json',
            data=dumps({}),
            headers=self.headers)
        expected = {
            'status': 'fail',
            'message': 'Not all fields were provided.',
            'missing': 'address, board_id'}
        actual = loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected, actual)
