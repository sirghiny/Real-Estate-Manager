"""Application commands."""

# pylint:disable=invalid-name, too-many-locals, too-many-statements

from os import environ, system

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from api.helpers.auth import create_token
from api.models import (db, Role, User)
from main import app

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def init():
    """Delete current migrations and recreate migrations."""
    system('rm -rf migrations')
    system('python manage.py db init')
    system('python manage.py db migrate')
    system('python manage.py db upgrade')
    print('\n Database ready for use.\n')


@manager.command
def seed_roles():
    """Add initial roles to the database."""
    Role.drop()
    roles = ['basic', 'admin', 'super_admin']
    for role in roles:
        new_role = Role(title=role)
        new_role.save()
    print('\nRoles Seeded.\n')


@manager.command
def create_test_token():
    """Create token for use in testing."""
    user = User.get(email="first1.last1@email.com")
    roles = Role.get_all()
    user.insert('roles', roles)
    user.save()
    token = create_token("first1.last1@email.com")
    environ['TEST_TOKEN'] = token
    print('\nToken created:\n', token,
          '\nThe token is saved in the environment.\n')


if __name__ == '__main__':
    manager.run()
