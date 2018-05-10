# pylint:disable=missing-docstring, invalid-name

from api.models import Deposit, Payment
from tests.base import BaseCase


class TestDeposit(BaseCase):

    def test_save_deposit(self):
        self.assertTrue(self.deposit1.save())

    def test_get_deposit(self):
        self.assertEqual(True, isinstance(Deposit.get(id=1), dict))
        self.deposit1.save()
        self.assertEqual(True, isinstance(Deposit.get(id=1), Deposit))

    def test_view_deposit(self):
        self.deposit1.save()
        deposit1 = Deposit.get(id=1)
        expected = ['id', 'amount', 'period_end',
                    'period_start', 'timestamp', 'payment_id']
        actual = list(deposit1.view().keys())
        self.assertEqual(expected, actual)

    def test_get_all_deposits(self):
        self.assertEqual(True, isinstance(Deposit.get(id=1), dict))
        self.deposit1.save()
        self.deposit2.save()
        self.assertEqual(True, isinstance(Deposit.get_all()[0], Deposit))
        self.assertEqual(True, isinstance(Deposit.get_all()[1], Deposit))
        self.assertEqual(2, len(Deposit.get_all()))

    def test_deposit_exists(self):
        self.assertFalse(Deposit.check_exists(id=1))
        self.deposit1.save()
        self.assertTrue(Deposit.check_exists(id=1))

    def test_delete_deposit(self):
        self.deposit1.save()
        self.assertTrue(Deposit.check_exists(id=1))
        deposit1 = Deposit.get(id=1)
        self.assertTrue(deposit1.delete())
        self.assertFalse(Deposit.check_exists(id=1))

    def test_add_and_remove_payment_to_deposit(self):
        self.deposit1.save()
        self.payment1.save()
        deposit1 = Deposit.get(id=1)
        self.assertEqual(None, deposit1.payment)
        deposit1.insert('payment', Payment.get(id=1))
        self.assertEqual(True, isinstance(deposit1.payment, Payment))
        deposit1.remove('payment')
        self.assertEqual(None, deposit1.payment)
