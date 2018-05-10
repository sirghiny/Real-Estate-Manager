"""
Unit manipulation functionality.
"""

from flask_restful import Resource


class UnitResource(Resource):
    """
    View functions for units.
    """

    def post(self):
        """
        Create a unit.
        """
        pass

    def get(self, unit_id=None):
        """
        Get unit(s).
        """
        pass

    def patch(self, unit_id):
        """
        Edit a unit.
        """
        pass

    def delete(self, unit_id):
        """
        Delete a unit.
        """
        pass


class UnitPaymentResource(Resource):
    """
    View functions for unit's payment.
    """

    def get(self, unit_id=None):
        """
        Get unit's payment details.
        """
        pass

    def delete(self, unit_id):
        """
        Delete a unit's payment details.
        """
        pass


class UnitResidentResource(Resource):
    """
    View functions for unit's resident.
    """

    def get(self, unit_id=None):
        """
        Get unit's resident details.
        """
        pass

    def patch(self, unit_id):
        """
        Edit a unit's resident details.
        """
        pass

    def delete(self, unit_id):
        """
        Delete a unit's resident details.
        """
        pass
