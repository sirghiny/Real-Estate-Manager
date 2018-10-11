"""Deposit."""

from time import time

from .base import BaseModel, db


class Deposit(BaseModel):
    """Deposit model."""

    id = db.Column(db.Integer(),
                   primary_key=True)
    amount = db.Column(db.Float(),
                       default=0.0)
    period_end = db.Column(db.Float(),
                           default=time())
    period_start = db.Column(db.Float(),
                             default=time())
    timestamp = db.Column(db.Float(),
                          default=time())
    payment_id = db.Column(db.Integer(),
                           db.ForeignKey('payment.id'),
                           nullable=True)

    def view(self):
        """Detailed view of a deposit."""
        return self.serialize()
