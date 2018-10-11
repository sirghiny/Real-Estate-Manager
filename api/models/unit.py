"""Unit."""

from .base import BaseModel, db


class Unit(BaseModel):
    """Unit model."""

    id = db.Column(db.Integer(),
                   primary_key=True)
    name = db.Column(db.String(),
                     nullable=False)
    payment = db.relationship('Payment',
                              backref='unit',
                              lazy=True,
                              uselist=False)
    board_id = db.Column(db.Integer(),
                         db.ForeignKey('board.id'),
                         nullable=True)
    estate_id = db.Column(db.Integer(),
                          db.ForeignKey('estate.id'),
                          nullable=True)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('user.id'),
                        nullable=True)

    def __repr__(self):
        """Summarized view of a unit."""
        return {'id': self.id, 'name': self.name,
                'estate': self.estate.__repr__()}

    def view(self):
        """Detailed view of a unit."""
        unit = self.serialize()
        unit.update({'board': self.board.__repr__()})
        unit.update({'estate': self.estate.__repr__()})
        unit.update({'payment': self.payment.__repr__()})
        unit.update({'resident': self.resident.__repr__()})
        return unit
