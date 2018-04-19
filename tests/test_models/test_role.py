# pylint:disable=missing-docstring, invalid-name

from     api.models import Role, User
from     tests.base import BaseCase


class TestRole(BaseCase):

    def test_save_role(self):
        self.assertTrue(self.role1.save())
        self.assertEqual(True, isinstance(self.role4.save(), dict))

    def test_get_role(self):
        self.assertEqual(True, isinstance(Role.get(id=1), dict))
        self.role1.save()
        self.assertEqual(True, isinstance(Role.get(id=1), Role))

    def test_get_many_roles(self):
        self.assertEqual(True, isinstance(Role.get_all(), dict))
        self.role1.save()
        self.role2.save()
        self.role3.save()
        self.assertEqual(True, isinstance(Role.get_all()[0], Role))
        self.assertEqual(True, isinstance(Role.get_all()[1], Role))
        self.assertEqual(3, len(Role.get_all()))

    def test_role_exists(self):
        self.assertFalse(Role.check_exists(id=1))
        self.role1.save()
        self.assertTrue(Role.check_exists(id=1))

    def test_add_and_remove_users_from_role(self):
        self.user1.save()
        self.user2.save()
        self.role1.save()
        role1 = Role.get(id=1)
        self.assertEqual(0, len(role1.users))
        users = User.get_all()
        role1.insert('users', users)
        self.assertEqual(True, isinstance(role1.users[0], User))
        role1.remove('users', id=1)
        self.assertEqual(1, len(role1.users))
        role1.remove('users')
        self.assertEqual(0, len(role1.users))

    def test_update_role(self):
        self.role1.save()
        role1 = Role.get(id=1)
        role1.update({'title': 'new_role_title'})
        self.assertEqual('new_role_title', Role.get(id=1).title)
        self.assertTrue(isinstance(
            role1.update({'random': 'bad field'}), dict))
