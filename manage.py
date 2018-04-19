"""
Application commands.
"""

# pylint:disable=invalid-name, too-many-locals, too-many-statements

from os import environ, system

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from api.helpers.auth import create_token
from api.helpers.general import digest
from api.models import (db, Board, Deposit, Estate, Conversation,
                        Message, Payment, Role, Unit, User, Wallet)
from main import app

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def init():
    """
    Delete current migrations.
    Recreate migrations.
    """
    system('rm -Rf migrations')
    system('python manage.py db init')
    system('python manage.py db migrate')
    system('python manage.py db upgrade')
    print('\n Database ready for use.\n')


@manager.command
def seed_roles():
    """
    Add initial roles to the database.
    """

    Role.drop()
    roles = ['basic', 'admin', 'super_admin']
    for role in roles:
        new_role = Role(title=role)
        new_role.save()
    print('\nRoles Seeded.\n')


@manager.command
def create_test_token():
    """
    Create token for use in testing.
    Seed roles before running this.
    """
    user = User.get(email="test.user@rem.com")
    roles = Role.get_all()
    user.insert('roles', roles)
    user.save()
    token = create_token("test.user@rem.com")
    environ['TEST_TOKEN'] = token
    print('\nToken created:\n', token,
          '\nThe token is saved in the environment.\n')


@manager.command
def seed_test_data():
    """
    Seed data to be used for testing.
    """
    db.drop_all()
    db.create_all()
    payment_1 = Payment()
    payment_2 = Payment()
    payment_3 = Payment()
    payment_4 = Payment()
    payment_1.insert('deposits', [Deposit(
        amount=1000.0), Deposit(amount=500.0)])
    payment_2.insert('deposits', [Deposit(
        amount=1000.0), Deposit(amount=500.0)])
    payment_3.insert('deposits', [Deposit(amount=1000.0)])
    payment_4.insert('deposits', [Deposit(amount=1000.0)])
    wallet_1 = Wallet()
    wallet_2 = Wallet()
    wallet_3 = Wallet()
    wallet_4 = Wallet()
    wallet_1.insert('payments', [payment_1, payment_2])
    wallet_2.insert('payments', [payment_3])
    wallet_3.insert('payments', [payment_4])
    estate1 = Estate(address='Casterly Rock')
    estate2 = Estate(address='Dorne')
    estate3 = Estate(address='Dragonstone')
    estate2.insert('payment', wallet_2.payments[0])
    estate3.insert('payment', wallet_3.payments[0])
    unit1 = Unit(name='No. 1')
    unit2 = Unit(name='No. 2')
    unit3 = Unit(name='No. 1')
    unit4 = Unit(name='No. 2')
    unit5 = Unit(name='No. 3')
    unit1.insert('payment', wallet_1.payments[0])
    unit2.insert('payment', wallet_1.payments[1])
    estate1.insert('estate_units', [unit1, unit2])
    estate2.insert('estate_units', [unit3])
    estate3.insert('estate_units', [unit4, unit5])
    board1 = Board()
    board2 = Board()
    board1.insert('estates_owned', [estate1, estate2])
    board2.insert('estates_owned', [estate3])
    board1.insert('units_owned', [unit5])
    user0 = User(
        name="Test User",
        phone_number="000 00 0000000",
        email="test.user@rem.com",
        password=digest('ABC123!@#1'))
    user1 = User(
        name="Jaime Lannister",
        phone_number="000 12 3456781",
        email="jaime.kingslayer@casterly.com",
        password=digest('ABC123!@#1'))
    user2 = User(
        name="Oberyn Martell",
        phone_number="000 12 3456782",
        email="oberyn.viper@dorne.com",
        password=digest('ABC123!@#2'))
    user3 = User(
        name="Daenerys Targaryen",
        phone_number="000 12 3456783",
        email="daenerys.khaleesi@dragonstone.com",
        password=digest('ABC123!@#3'))
    conversation1 = Conversation()
    conversation2 = Conversation()
    message1 = Message(sender=user1.name,
                       content='Content 1')
    message2 = Message(sender=user2.name,
                       content='Content 2')
    message3 = Message(sender=user3.name,
                       content='Content 3')
    conversation1.insert('messages', [message1, message2])
    conversation2.insert('messages', [message3])
    user0.insert('boards', [board1])
    user1.insert('boards', [board1])
    user2.insert('boards', [board1])
    user3.insert('boards', [board2])
    user1.insert('units', [unit1, unit2])
    user2.insert('units', [unit3])
    user3.insert('units', [unit4])
    user0.insert('wallet', wallet_4)
    user1.insert('wallet', wallet_1)
    user2.insert('wallet', wallet_2)
    user3.insert('wallet', wallet_3)
    user1.insert('conversations', [conversation1, conversation2])
    user2.insert('conversations', [conversation1, conversation2])
    user3.insert('conversations', [conversation1])
    role1 = Role(title='admin')
    role2 = Role(title='basic')
    role3 = Role(title='super_admin')
    role3.insert('users', [user0, user1])
    role2.insert('users', [user0, user1, user2, user3])
    role1.insert('users', [user0, user3])
    role1.save()
    role2.save()
    role3.save()
    print('\nTest Data Seeded.\n')


if __name__ == '__main__':
    manager.run()
