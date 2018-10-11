"""Conversation."""

from operator import itemgetter
from time import time

from .base import BaseModel, db


class Conversation(BaseModel):
    """Conversation model."""

    id = db.Column(db.Integer(),
                   primary_key=True)
    timestamp = db.Column(db.Float(),
                          default=time())
    title = db.Column(db.String(),
                      nullable=True)
    messages = db.relationship('Message',
                               backref='conversation',
                               lazy=True,
                               uselist=True,
                               cascade="all,delete")
    board_id = db.Column(db.Integer(),
                         db.ForeignKey('board.id'),
                         nullable=True)

    def __repr__(self):
        """Summarized view of a conversation."""
        try:
            last_message = self.messages[-1].view()
        except IndexError:
            last_message = None
        return {
            'title': self.title,
            'last_message': last_message
        }

    def view(self):
        """Detailed view of a conversation."""
        conversation = self.serialize()
        conversation.update({'participants': [i.__repr__()
                                              for i in self.participants]})
        conversation.update(
            {'messages': sorted(
                [i.serialize() for i in self.messages],
                key=itemgetter('timestamp'))})
        return conversation
