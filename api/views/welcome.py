"""Welcome to the API functionality."""

from flask_restful import Resource

# pylint:disable=no-self-use


class WelcomeResource(Resource):
    """Displays welcome message and any other introductory information."""

    def get(self):
        """Get the welcome message an display it."""
        return {
            'status': 'success',
            'data': {
                'message': 'Welcome to Real Estate Manager.'
            }
        }, 200
