"""Estate."""
from .base import BaseModel, db


class Estate(BaseModel):
    """Estate model."""

    id = db.Column(db.Integer(),
                   primary_key=True)
    address = db.Column(db.String(),
                        nullable=False)
    estate_units = db.relationship('Unit',
                                   backref='estate',
                                   lazy=True,
                                   uselist=True)
    payment = db.relationship('Payment',
                              backref='estate',
                              lazy=True,
                              uselist=False)
    board_id = db.Column(db.Integer(),
                         db.ForeignKey('board.id'),
                         nullable=True)

    def __repr__(self):
        """Summarized view of an estate."""
        return {'id': self.id, 'address': self.address}

    def view(self):
        """Detailed view of an estate."""
        estate = self.serialize()
        estate.update({'board': self.board.__repr__()})
        estate.update({'payment': self.payment.__repr__()})
        estate.update({'units': [unit.view() for unit in self.estate_units]})
        return estate
