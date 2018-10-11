"""Payment."""

from .base import BaseModel, db


class Payment(BaseModel):
    """Payment model."""

    id = db.Column(db.Integer(),
                   primary_key=True)
    balance = db.Column(db.Float(),
                        default=0.0)
    required = db.Column(db.Float(),
                         default=0.0)
    deposits = db.relationship('Deposit',
                               backref='payment',
                               lazy=True,
                               uselist=True,
                               cascade="all,delete")
    estate_id = db.Column(db.Integer(),
                          db.ForeignKey('estate.id'),
                          nullable=True)
    unit_id = db.Column(db.Integer(),
                        db.ForeignKey('unit.id'),
                        nullable=True)
    wallet_id = db.Column(db.Integer(),
                          db.ForeignKey('wallet.id'),
                          nullable=True)

    def __repr__(self):
        """Summarized view of a payment."""
        return {
            'id': self.id,
            'required': self.required,
            'balance': self.balance
        }

    def view(self):
        """Detailed view of a payment."""
        payment = self.serialize()
        deposits = [i.view() for i in self.deposits]
        payment.update({'deposits': deposits})
        return payment
