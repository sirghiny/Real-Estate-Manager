# pylint:disable=missing-docstring, invalid-name

from api.models import Payment, User, Wallet
from tests.base import BaseCase


class TestWallet(BaseCase):

    def test_save_wallet(self):
        self.assertTrue(self.wallet1.save())

    def test_get_wallet(self):
        self.assertEqual(True, isinstance(Wallet.get(id=1), dict))
        self.wallet1.save()
        self.assertEqual(True, isinstance(Wallet.get(id=1), Wallet))

    def test_get_many_wallets(self):
        self.assertEqual(True, isinstance(Wallet.get(id=1), dict))
        self.wallet1.save()
        self.wallet2.save()
        self.assertEqual(True, isinstance(Wallet.get_all()[0], Wallet))
        self.assertEqual(True, isinstance(Wallet.get_all()[1], Wallet))
        self.assertEqual(2, len(Wallet.get_all()))

    def test_wallet_exists(self):
        self.assertFalse(Wallet.check_exists(id=1))
        self.wallet1.save()
        self.assertTrue(Wallet.check_exists(id=1))

    def test_add_and_remove_payments_from_wallet(self):
        self.wallet1.save()
        self.payment1.save()
        self.payment2.save()
        wallet1 = Wallet.get(id=1)
        self.assertEqual(0, len(wallet1.payments))
        wallet1.insert('payments', [Payment.get(id=1), Payment.get(id=2)])
        wallet1 = Wallet.get(id=1)
        self.assertEqual(True, isinstance(wallet1.payments[0], Payment))
        self.assertEqual(True, isinstance(wallet1.payments[1], Payment))
        self.assertEqual(2, len(wallet1.payments))
        wallet1.remove('payments', id=1)
        self.assertEqual(1, len(wallet1.payments))

    def test_add_and_remove_wallet_owner(self):
        self.user1.save()
        self.wallet1.save()
        wallet1 = Wallet.get(id=1)
        wallet1.insert('owner', User.get(id=1))
        self.assertEqual(True, isinstance(wallet1.owner, User))
        wallet1.insert('owner', None)
        self.assertEqual(None, wallet1.owner)

    def test_update_wallet(self):
        self.wallet1.save()
        wallet1 = Wallet.get(id=1)
        wallet1.update({'balance': 1000.0})
        self.assertEqual(1000.0, Wallet.get(id=1).balance)
        self.assertTrue(isinstance(
            wallet1.update({'random': 'bad field'}), dict))
