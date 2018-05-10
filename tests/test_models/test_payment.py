# pylint:disable=missing-docstring, invalid-name

from api.models import Deposit, Estate, Payment, Unit, Wallet
from tests.base import BaseCase


class TestPayment(BaseCase):

    def test_save_payment(self):
        self.assertTrue(self.payment1.save())

    def test_get_payment(self):
        self.assertEqual(True, isinstance(Payment.get(id=1), dict))
        self.payment1.save()
        self.assertEqual(True, isinstance(Payment.get(id=1), Payment))

    def test_get_many_payments(self):
        self.assertEqual(True, isinstance(Payment.get(id=1), dict))
        self.payment1.save()
        self.payment2.save()
        self.assertEqual(True, isinstance(Payment.get_all()[0], Payment))
        self.assertEqual(True, isinstance(Payment.get_all()[1], Payment))
        self.assertEqual(2, len(Payment.get_all()))

    def test_payment_exists(self):
        self.assertFalse(Payment.check_exists(id=1))
        self.payment1.save()
        self.assertTrue(Payment.check_exists(id=1))

    def test_repr_payment(self):
        self.payment1.save()
        payment1 = Payment.get(id=1)
        expected = ['id', 'required', 'balance']
        actual = list(payment1.__repr__().keys())
        self.assertEqual(expected, actual)

    def test_delete_payment(self):
        self.payment1.save()
        self.assertTrue(Payment.check_exists(id=1))
        payment1 = Payment.get(id=1)
        self.assertTrue(payment1.delete())
        self.assertFalse(Payment.check_exists(id=1))

    def test_update_payment(self):
        self.payment1.save()
        payment1 = Payment.get(id=1)
        payment1.update({'balance': 1000.0, 'required': 5000.0})
        payment1 = Payment.get(id=1)
        self.assertEqual(1000.0, payment1.balance)
        self.assertEqual(5000.0, payment1.required)
        self.assertTrue(isinstance(
            payment1.update({'random': 'bad field'}), dict))

    def test_add_and_remove_deposit_estate_unit_wallet(self):
        self.deposit1.save()
        self.deposit2.save()
        self.estate1.save()
        self.unit1.save()
        self.wallet1.save()
        self.payment1.save()
        payment1 = Payment.get(id=1)
        payment1.estate = Estate.get(id=1)
        payment1.unit = Unit.get(id=1)
        payment1.wallet = Wallet.get(id=1)
        payment1.insert('deposits', [Deposit.get(id=1), Deposit.get(id=2)])
        self.assertEqual(True, isinstance(payment1.estate, Estate))
        self.assertEqual(True, isinstance(payment1.unit, Unit))
        self.assertEqual(True, isinstance(payment1.wallet, Wallet))
        self.assertEqual(True, isinstance(payment1.deposits[0], Deposit))
        self.assertEqual(True, isinstance(payment1.deposits[1], Deposit))
        self.assertEqual(2, len(payment1.deposits))
        payment1.remove('estate')
        payment1.remove('unit')
        payment1.remove('wallet')
        self.assertEqual(None, payment1.estate)
        self.assertEqual(None, payment1.unit)
        self.assertEqual(None, payment1.wallet)
        payment1.remove('deposits', id=1)
        self.assertEqual(1, len(payment1.deposits))
