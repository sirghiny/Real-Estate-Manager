# pylint:disable=missing-docstring, invalid-name

from api.models import Board, Conversation, Estate, Unit, User
from tests.base import BaseCase


class TestBoard(BaseCase):

    def test_save_board(self):
        self.assertEqual(1, self.board1.save())

    def test_add_and_remove_users_from_board(self):
        self.board1.save()
        self.user1.save()
        self.user2.save()
        board1 = Board.get(id=1)
        board1.insert('members', [User.get(id=1), User.get(id=2)])
        self.assertEqual(2, len(Board.get(id=1).members))
        board1.remove('members', id=1)
        self.assertEqual(1, len(Board.get(id=1).members))

    def test_get_board(self):
        self.board1.save()
        self.assertTrue(isinstance(Board.get(id=1), Board))

    def test_get_many_boards(self):
        self.assertTrue(isinstance(Board.get_all(), dict))
        self.board1.save()
        self.board2.save()
        self.assertEqual(2, len(Board.get_all()))

    def test_repr_board(self):
        self.board1.save()
        board1 = Board.get(id=1)
        expected = ['id', 'members']
        actual = [key for key in board1.__repr__()]
        self.assertEqual(expected, actual)

    def test_board_exists(self):
        self.board1.save()
        self.assertEqual(True, Board.check_exists(id=1))
        self.assertEqual(False, Board.check_exists(id=2))

    def test_add_remove_conversation_from_board(self):
        self.board1.save()
        self.conversation1.save()
        board1 = Board.get(id=1)
        board1.insert('conversation', Conversation.get(id=1))
        self.assertEqual(True, isinstance(board1.conversation, Conversation))
        board1.remove('conversation')
        self.assertEqual(None, board1.conversation)

    def test_add_and_remove_units_owned_to_board(self):
        self.board1.save()
        self.unit1.save()
        self.unit2.save()
        board1 = Board.get(id=1)
        board1.insert('units_owned', [Unit.get(id=1), Unit.get(id=2)])
        units = Board.get(id=1).units_owned
        self.assertEqual("Random Unit 1", units[0].name)
        self.assertEqual("Random Unit 2", units[1].name)
        self.assertEqual(2, len(units))
        self.assertEqual(True, isinstance(units[0], Unit))
        self.assertEqual(True, isinstance(units[1], Unit))
        board1.remove('units_owned', id=1)
        self.assertEqual(1, len(Board.get(id=1).units_owned))

    def test_add_and_remove_estates_owned_to_board(self):
        self.board1.save()
        self.estate1.save()
        self.estate2.save()
        board1 = Board.get(id=1)
        board1.insert('estates_owned', [Estate.get(id=1), Estate.get(id=2)])
        estates = Board.get(id=1).estates_owned
        self.assertEqual("Random Address 1", estates[0].address)
        self.assertEqual("Random Address 2", estates[1].address)
        self.assertEqual(2, len(estates))
        self.assertEqual(True, isinstance(estates[0], Estate))
        self.assertEqual(True, isinstance(estates[1], Estate))
        board1.remove('estates_owned', id=1)
        self.assertEqual(1, len(Board.get(id=1).estates_owned))

    def test_delete_board(self):
        self.board1.save()
        self.estate1.save()
        self.unit1.save()
        board1 = Board.get(id=1)
        board1.insert('estates_owned', [Estate.get(id=1)])
        board1.units_owned.append(Unit.get(id=1))
        self.assertEqual(True, Board.get(id=1).delete())
        self.assertEqual(True, isinstance(Board.get(id=1), dict))
