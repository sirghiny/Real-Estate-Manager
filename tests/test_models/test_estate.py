# pylint:disable=missing-docstring, invalid-name

from api.models import Board, Estate, Payment, Unit
from tests.base import BaseCase


class TestEstate(BaseCase):

    def test_save_estate(self):
        self.assertTrue(self.estate1.save())
        self.assertEqual(True, isinstance(self.estate3.save(), dict))

    def test_get_estate(self):
        self.assertEqual(True, isinstance(Estate.get(id=1), dict))
        self.estate1.save()
        self.assertEqual(True, isinstance(Estate.get(id=1), Estate))

    def test_get_many_estates(self):
        self.assertEqual(True, isinstance(Estate.get(id=1), dict))
        self.estate1.save()
        self.estate2.save()
        self.assertEqual(True, isinstance(Estate.get_all()[0], Estate))
        self.assertEqual(True, isinstance(Estate.get_all()[1], Estate))
        self.assertEqual(2, len(Estate.get_all()))

    def test_estate_exists(self):
        self.assertFalse(Estate.check_exists(id=1))
        self.estate1.save()
        self.assertTrue(Estate.check_exists(id=1))

    def test_repr_estate(self):
        self.estate1.save()
        estate1 = Estate.get(id=1)
        expected = ['id', 'address']
        actual = [key for key in estate1.__repr__()]
        self.assertEqual(expected, actual)

    def test_add_and_remove_units_from_estate(self):
        self.estate1.save()
        self.unit1.save()
        self.unit2.save()
        estate1 = Estate.get(id=1)
        self.assertEqual(0, len(estate1.estate_units))
        estate1.insert('estate_units', Unit.get(id=1), Unit.get(id=2))
        self.assertEqual(2, len(estate1.estate_units))
        self.assertEqual(True, isinstance(estate1.estate_units[0], Unit))
        self.assertEqual(True, isinstance(estate1.estate_units[1], Unit))
        estate1.remove('estate_units', id=1)
        self.assertEqual(1, len(estate1.estate_units))

    def test_add_and_remove_payment_to_estate(self):
        self.estate1.save()
        self.payment1.save()
        estate1 = Estate.get(id=1)
        self.assertEqual(None, estate1.payment)
        payment1 = Payment.get(id=1)
        estate1.insert('payment', payment1)
        estate1 = Estate.get(id=1)
        self.assertEqual(True, isinstance(estate1.payment, Payment))
        estate1.remove('payment')
        self.assertEqual(None, estate1.payment)

    def test_get_estate_board(self):
        self.estate1.save()
        self.board1.save()
        board1 = Board.get(id=1)
        board1.insert('estates_owned', Estate.get(id=1))
        estate1 = Estate.get(id=1)
        self.assertEqual(1, estate1.board_id)
