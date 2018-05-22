"""
Estate manipulation functionality.
"""

from flask import request
from flask_restful import Resource

from api.helpers.modelops import get_boards, get_estates
from api.helpers.validation import validate_json
from api.models import Board, Estate


class EstateResource(Resource):
    """
    View functions for estates.
    """

    def get(self, estate_id=None):
        """
        View an estate(s).
        """
        result = get_estates(estate_id)
        if isinstance(result, dict):
            return result, 404
        elif isinstance(result, list):
            return {
                'status': 'success',
                'data': {'estates': [estate.view() for estate in result]}
            }, 200
        else:
            return {
                'status': 'success',
                'data': {'estate': result.view()}
            }, 200

    def post(self):
        """
        Create an estate.
        """
        payload = request.get_json()
        required = ['address', 'board_id']
        result = validate_json(required, payload)
        if isinstance(result, bool) is True:
            board = get_boards(payload['board_id'])
            if isinstance(board, dict):
                return board, 404
            else:
                new_estate = Estate(
                    address=payload['address'])
                new_id = new_estate.save()
                board.insert('estates_owned', [Estate.get(id=new_id)])
                return {
                    'status': 'success',
                    'message': 'Estate with id {} created.'.format(new_id)
                }, 201
        else:
            return {
                'status': 'fail',
                'message': 'Not all fields were provided.',
                'missing': result
            }, 400

    def patch(self, estate_id):
        """
        Edit an estate.
        """
        pass

    def delete(self, estate_id):
        """
        Delete an estate.
        """
        pass


class EstatePaymentResource(Resource):
    """
    View functions for estate payments.
    """

    def get(self, estate_id):
        """
        View an estate's payment details.
        """
        result = get_estates(estate_id)
        if isinstance(result, dict):
            return result, 404
        else:
            payment = result.payment.view()
            return {
                'status': 'success',
                'data': {'payment': payment}
            }, 200

    def patch(self):
        """
        Make a deposit for an estate's payment.
        """
        pass

    def delete(self, estate_id):
        """
        Clear an estate's payment history.
        """
        pass


class EstateUnitsResource(Resource):
    """
    View functions for estate units.
    """

    def get(self, unit_id=None):
        """
        Get estate unit(s).
        """
        pass

    def patch(self, estate_id):
        """
        Edit an estate's units.
        """
        pass
