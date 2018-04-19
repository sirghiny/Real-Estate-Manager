# pylint:disable=missing-docstring, invalid-name

from api.models import Message
from tests.base import BaseCase


class TestMessage(BaseCase):

    def test_save_message(self):
        self.assertTrue(self.message1.save())
        self.assertEqual(True, isinstance(self.message3.save(), dict))

    def test_get_message(self):
        self.assertEqual(True, isinstance(Message.get(id=1), dict))
        self.message1.save()
        self.assertEqual(True, isinstance(
            Message.get(id=1), Message))

    def test_get_all_messages(self):
        self.assertEqual(True, isinstance(Message.get(id=1), dict))
        self.message1.save()
        self.message2.save()
        self.assertEqual(True, isinstance(
            Message.get_all()[0], Message))
        self.assertEqual(True, isinstance(
            Message.get_all()[1], Message))
        self.assertEqual(2, len(Message.get_all()))

    def test_message_exists(self):
        self.assertFalse(Message.check_exists(id=1))
        self.message1.save()
        self.assertTrue(Message.check_exists(id=1))

    def test_delete_message(self):
        self.message1.save()
        message1 = Message.get(id=1)
        self.assertTrue(message1.delete())
        self.assertFalse(Message.check_exists(id=1))

    def test_update_message(self):
        self.message1.save()
        message1 = Message.get(id=1)
        message1.update({'content': 'new_content'})
        self.assertEqual('new_content', Message.get(id=1).content)
        self.assertTrue(isinstance(
            message1.update({'random': 'bad field'}), dict))
