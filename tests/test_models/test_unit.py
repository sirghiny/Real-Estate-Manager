# pylint:disable=missing-docstring, invalid-name


from api.models import Board, Estate, Payment, Unit, User
from tests.base import BaseCase


class TestUnit(BaseCase):

    def test_save_unit(self):
        self.assertTrue(self.unit1.save())
        self.assertEqual(True, isinstance(self.unit3.save(), dict))

    def test_get_unit(self):
        self.assertEqual(True, isinstance(Unit.get(id=1), dict))
        self.unit1.save()
        self.assertEqual(True, isinstance(Unit.get(id=1), Unit))

    def test_get_many_units(self):
        self.assertEqual(True, isinstance(Unit.get_all(), dict))
        self.unit1.save()
        self.unit2.save()
        self.assertEqual(True, isinstance(Unit.get_all()[0], Unit))
        self.assertEqual(True, isinstance(Unit.get_all()[1], Unit))
        self.assertEqual(2, len(Unit.get_all()))

    def test_unit_exists(self):
        self.assertFalse(Unit.check_exists(id=1))
        self.unit1.save()
        self.assertTrue(Unit.check_exists(id=1))

    def test_add_and_remove_payment_from_unit(self):
        self.unit1.save()
        self.payment1.save()
        unit1 = Unit.get(id=1)
        self.assertEqual(None, unit1.payment)
        payment1 = Payment.get(id=1)
        unit1.insert('payment', payment1)
        unit1 = Unit.get(id=1)
        self.assertEqual(True, isinstance(unit1.payment, Payment))
        unit1.remove('payment')
        self.assertEqual(None, unit1.payment)

    def test_add_and_remove_board_estate_resident(self):
        self.board1.save()
        self.estate1.save()
        self.user1.save()
        self.unit1.save()
        unit1 = Unit.get(id=1)
        unit1.insert('resident', User.get(id=1))
        unit1.insert('board', Board.get(id=1))
        unit1.insert('estate', Estate.get(id=1))
        self.assertEqual(True, isinstance(unit1.board, Board))
        self.assertEqual(True, isinstance(unit1.resident, User))
        self.assertEqual(True, isinstance(unit1.estate, Estate))
        unit1.remove('resident')
        unit1.remove('board')
        unit1.remove('estate')
        self.assertEqual(None, unit1.board)
        self.assertEqual(None, unit1.estate)
        self.assertEqual(None, unit1.resident)

    def test_update_unit(self):
        self.unit1.save()
        unit1 = Unit.get(id=1)
        unit1.update({'name': 'new_unit_name'})
        self.assertEqual('new_unit_name', Unit.get(id=1).name)
        self.assertTrue(isinstance(
            unit1.update({'random': 'bad field'}), dict))
