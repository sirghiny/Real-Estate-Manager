"""Board."""
from .base import BaseModel, db


class Board(BaseModel):
    """Board model."""

    id = db.Column(db.Integer(),
                   primary_key=True)
    estates_owned = db.relationship('Estate',
                                    backref='board',
                                    lazy=True,
                                    uselist=True)
    units_owned = db.relationship('Unit',
                                  backref='board',
                                  lazy=True,
                                  uselist=True)
    conversation = db.relationship('Conversation',
                                   backref='board',
                                   lazy=True,
                                   uselist=False,
                                   cascade="all,delete")

    def __repr__(self):
        """Summarized view of a board."""
        return {
            'id': self.id,
            'members': [i.__repr__() for i in self.members]
        }

    def view(self):
        """Detailed view of a board."""
        board = self.serialize()
        board.update({'members': [i.__repr__() for i in self.members]})
        board.update({'estates_owned': [i.__repr__()
                                        for i in self.estates_owned]})
        board.update({'units_owned': [i.__repr__() for i in self.units_owned]})
        return board
