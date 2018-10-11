"""Message."""
from time import time

from .base import BaseModel, db


class Message(BaseModel):
    """Message model."""

    id = db.Column(db.Integer(),
                   primary_key=True)
    content = db.Column(db.String(),
                        nullable=True)
    edited = db.Column(db.Boolean(),
                       default=False)
    sender = db.Column(db.Integer(),
                       nullable=False)
    timestamp = db.Column(db.Float(),
                          default=time())
    conversation_id = db.Column(db.Integer(),
                                db.ForeignKey('conversation.id'),
                                nullable=True)

    def view(self):
        """Detailed view of a message."""
        return self.serialize()
