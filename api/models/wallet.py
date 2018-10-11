"""Wallet."""

from .base import BaseModel, db


class Wallet(BaseModel):
    """Wallet model."""

    id = db.Column(db.Integer(),
                   primary_key=True)
    balance = db.Column(db.Float(),
                        default=0.0)
    payments = db.relationship('Payment',
                               backref='wallet',
                               lazy=True,
                               uselist=True)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('user.id'),
                        nullable=True)

    def __repr__(self):
        """Summarized view of a wallet."""
        return {
            'id': self.id,
            'balance': self.balance
        }

    def view(self):
        """Detailed view of a wallet."""
        wallet = self.serialize()
        payments = [i.view() for i in self.payments]
        wallet.update({'payments': payments})
        return wallet
