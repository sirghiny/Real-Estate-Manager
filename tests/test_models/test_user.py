# pylint:disable=missing-docstring, invalid-name

from api.models import Board, Conversation, Role, User
from tests.base import BaseCase


class TestUser(BaseCase):

    def test_save_user(self):
        self.assertEqual(1, self.user1.save())
        self.assertTrue(isinstance(self.user3.save(), dict))

    def test_get_user(self):
        self.user1.save()
        self.assertTrue(isinstance(User.get(id=1), User))
        self.assertTrue(isinstance(User.get(id=2), dict))

    def test_get_many_users(self):
        self.assertTrue(isinstance(User.get_all(), dict))
        self.user1.save()
        self.user2.save()
        self.assertEqual(2, len(User.get_all()))

    def test_check_user_exists(self):
        self.user1.save()
        self.assertEqual(True, User.check_exists(id=1))
        self.assertEqual(False, User.check_exists(id=2))

    def test_delete_user(self):
        self.user1.save()
        self.assertEqual(True, User.get(id=1).delete())
        self.assertTrue(isinstance(User.get(id=1), dict))

    def test_search_user_when_none_exist(self):
        self.assertTrue(isinstance(User.search(name='random'), dict))

    def test_search_user_single_result(self):
        self.user1.save()
        self.user2.save()
        actual = User.search(name='Middle2')
        self.assertEqual(1, len(actual))
        self.assertTrue(isinstance(actual[0], User))
        self.assertEqual('First2 Middle2 Last2', actual[0].name)

    def test_search_user_multiple_results(self):
        self.user1.save()
        self.user2.save()
        actual = User.search(name='Middle')
        self.assertEqual(2, len(actual))
        self.assertTrue(isinstance(actual[0], User))
        self.assertTrue(isinstance(actual[1], User))

    def test_update_user(self):
        self.user1.save()
        user1 = User.get(id=1)
        user1.update(self.user_new_data1)
        self.assertEqual('000 12 3456783', User.get(id=1).phone_number)
        self.assertTrue(isinstance(user1.update(self.user_new_data2), dict))

    def test_serialize_user_object(self):
        self.user1.save()
        excepted = sorted(['id', 'name', 'password', 'phone_number', 'email'])
        actual = sorted([key for key in User.get(id=1).serialize()])
        self.assertEqual(excepted, actual)

    def test_view_public_user(self):
        self.user1.save()
        excepted = {
            'id': 1,
            'email': 'first1.last1@email.com',
            'name': 'First1 Middle1 Last1',
            'phone_number': '000 12 3456781'}
        actual = User.get(id=1).view_public()
        self.assertDictEqual(excepted, actual)

    def test_view_private_user(self):
        self.assertTrue(isinstance(User.get(id=1), dict))
        self.user1.save()
        user1 = User.get(id=1)
        user1.insert('wallet', self.wallet1)
        user1.insert('conversations', [self.conversation1])
        user1.save()
        excepted = sorted(['id', 'email', 'name', 'phone_number',
                           'roles', 'wallet', 'conversations', 'boards'])
        actual = sorted(list(user1.view_private().keys()))
        self.assertEqual(excepted, actual)

    def test_insert_wrong_field(self):
        self.user1.save()
        self.board1.save()
        user1 = User.get(id=1)
        excepted = {
            "message": "Ensure the  field passed is valid.",
            "help": "The field should be an attribute of the object."
        }
        actual = user1.insert('random', Board.get_all())
        self.assertDictEqual(excepted, actual)

    def test_insert_wrong_values(self):
        self.user1.save()
        user1 = User.get(id=1)
        excepted = "Ensure the values you're inserting are valid."
        actual = user1.insert('boards', [{}])["message"]
        self.assertEqual(excepted, actual)

    def test_insert_many_not_list(self):
        self.user1.save()
        self.board1.save()
        user1 = User.get(id=1)
        excepted = {
            "message": "Ensure objects passed are as a list.",
            "help": "This eases updating of (one)many-to-many fields"
        }
        actual = user1.insert('boards', Board.get(id=1))
        self.assertDictEqual(excepted, actual)

    def test_remove_wrong_field(self):
        self.user1.save()
        user1 = User.get(id=1)
        excepted = {
            "message": "Ensure the  field passed is valid.",
            "help": "The field should be an attribute of the object."
        }
        actual = user1.remove('random')
        self.assertDictEqual(excepted, actual)

    def test_add_and_remove_board_from_user(self):
        self.user1.save()
        self.board1.save()
        self.board2.save()
        user1 = User.get(id=1)
        self.assertEqual(0, len(user1.boards))
        user1.insert('boards', Board.get_all())
        self.assertEqual(2, len(user1.boards))
        user1.remove('boards', id=1)
        self.assertEqual(1, len(user1.boards))
        user1.remove('boards')
        self.assertEqual(0, len(user1.boards))

    def test_remove_wrong_kwargs(self):
        self.user1.save()
        self.conversation1.save()
        self.conversation2.save()
        user1 = User.get(id=1)
        excepted = 'Ensure the arguments passed are valid.'
        actual = user1.remove('conversations', id=3)['message']
        self.assertEqual(excepted, actual)

    def test_delete_all_users(self):
        self.user1.save()
        self.user2.save()
        self.assertEqual(2, len(User.get_all()))
        User.drop()
        self.assertTrue(isinstance(User.get_all(), dict))

    def test_add_and_remove_conversation_from_user(self):
        self.user1.save()
        self.conversation1.save()
        self.conversation2.save()
        user1 = User.get(id=1)
        self.assertEqual(0, len(user1.conversations))
        user1.insert('conversations', Conversation.get_all())
        self.assertEqual(2, len(user1.conversations))
        user1.remove('conversations', id=1)
        self.assertEqual(1, len(user1.conversations))
        user1.remove('conversations')
        self.assertEqual(0, len(user1.conversations))

    def test_add_and_remove_role_from_user(self):
        self.user1.save()
        self.role1.save()
        self.role2.save()
        user1 = User.get(id=1)
        self.assertEqual(0, len(user1.roles))
        user1.insert('roles', Role.get_all())
        self.assertEqual(2, len(user1.roles))
        user1.remove('roles', id=1)
        self.assertEqual(1, len(user1.roles))
        user1.remove('roles')
        self.assertEqual(0, len(user1.roles))
