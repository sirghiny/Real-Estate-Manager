# pylint:disable=missing-docstring, invalid-name


from api.helpers.auth import decrypt, encrypt, create_token
from api.helpers.general import digest, is_substring
from api.helpers.validation import validate_json
from tests.base import BaseCase


class TestHelpers(BaseCase):
    """
    Helpers test cases.
    """

    def test_validate_json(self):
        self.assertTrue(validate_json(['a', 'b'], {'a': True, 'b': False}))
        self.assertEqual(validate_json(['a', 'b'], {'a': True}), 'b')
        self.assertEqual(validate_json(['a', 'b'], {'a': True, 'b': ''}), 'b')
        self.assertEqual(validate_json(
            ['a', 'b'], {'a': True, 'b': None}), 'b')

    def test_is_substring(self):
        self.assertTrue(is_substring('First', 'FirstOne'))
        self.assertFalse(is_substring('First', 'SecondOne'))

    def test_digest(self):
        self.assertEqual(128, len(digest('a')))
