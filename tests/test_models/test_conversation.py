# pylint:disable=missing-docstring, invalid-name

from api.models import Conversation, Message
from tests.base import BaseCase


class TestConversation(BaseCase):

    def test_save_conversation(self):
        self.assertTrue(self.conversation1.save())

    def test_get_conversation(self):
        self.assertEqual(True, isinstance(Conversation.get(id=1), dict))
        self.conversation1.save()
        self.assertEqual(True, isinstance(
            Conversation.get(id=1), Conversation))

    def test_get_all_conversations(self):
        self.assertEqual(True, isinstance(Conversation.get(id=1), dict))
        self.conversation1.save()
        self.conversation2.save()
        self.assertEqual(True, isinstance(
            Conversation.get_all()[0], Conversation))
        self.assertEqual(True, isinstance(
            Conversation.get_all()[1], Conversation))
        self.assertEqual(2, len(Conversation.get_all()))

    def test_conversation_exists(self):
        self.assertFalse(Conversation.check_exists(id=1))
        self.conversation1.save()
        self.assertTrue(Conversation.check_exists(id=1))

    def test_repr_conversation(self):
        self.conversation1.save()
        conversation1 = Conversation.get(id=1)
        expected = ['title', 'last_message']
        actual = list(conversation1.__repr__().keys())
        self.assertEqual(expected, actual)

    def test_add_and_remove_message_from_conversation(self):
        self.conversation1.save()
        self.message1.save()
        self.message2.save()
        conversation1 = Conversation.get(id=1)
        self.assertEqual(0, len(conversation1.messages))
        conversation1.insert(
            'messages', Message.get(id=1), Message.get(id=2))
        self.assertEqual(True, isinstance(conversation1.messages[0], Message))
        self.assertEqual(True, isinstance(conversation1.messages[1], Message))
        self.assertEqual(2, len(conversation1.messages))
        conversation1.remove('messages', id=1)
        self.assertEqual(1, len(conversation1.messages))

    def test_delete_conversation(self):
        self.conversation1.save()
        conversation1 = Conversation.get(id=1)
        self.assertTrue(conversation1.delete())
        self.assertFalse(Conversation.check_exists(id=1))
