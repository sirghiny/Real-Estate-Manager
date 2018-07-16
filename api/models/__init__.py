"""Models definitions."""

from operator import itemgetter
from time import time

from .base import BaseModel, db


# Association tables.
user_conversations = db.Table(
    'user_conversations',
    db.Column(
        'user_id',
        db.Integer(),
        db.ForeignKey('user.id'),
        nullable=False),
    db.Column(
        'conversation_id',
        db.Integer(),
        db.ForeignKey('conversation.id'),
        nullable=False))

user_boards = db.Table(
    'user_boards',
    db.Column(
        'user_id',
        db.Integer(),
        db.ForeignKey('user.id'),
        nullable=False),
    db.Column(
        'board_id',
        db.Integer(),
        db.ForeignKey('board.id'),
        nullable=False))

user_roles = db.Table(
    'user_roles',
    db.Column(
        'user_id',
        db.Integer(),
        db.ForeignKey('user.id'),
        nullable=False),
    db.Column(
        'role_id',
        db.Integer(),
        db.ForeignKey('role.id'),
        nullable=False))


# Regular tables.
class User(BaseModel):
    """User's model."""

    id = db.Column(db.Integer(),
                   primary_key=True)
    email = db.Column(db.String(),
                      unique=True)
    name = db.Column(db.String(),
                     nullable=False)
    password = db.Column(db.String(),
                         nullable=False)
    phone_number = db.Column(db.String(),
                             nullable=False,
                             unique=True)
    boards = db.relationship('Board',
                             secondary='user_boards',
                             backref=db.backref('members',
                                                lazy=True,
                                                uselist=True))
    conversations = db.relationship('Conversation',
                                    secondary='user_conversations',
                                    backref=db.backref('participants',
                                                       lazy=True,
                                                       uselist=True))
    roles = db.relationship('Role',
                            secondary='user_roles',
                            backref=db.backref('users',
                                               lazy=True,
                                               uselist=True))
    units = db.relationship('Unit',
                            backref='resident',
                            lazy=True,
                            uselist=True)
    wallet = db.relationship('Wallet',
                             backref='owner',
                             lazy=True,
                             uselist=False,
                             cascade="all,delete")

    def __repr__(self):
        """Summarized view of a user."""
        user = self.serialize()
        del user['password']
        return user

    def view(self):
        """Detailed view of a user."""
        boards = [board.serialize() for board in self.boards]
        conversations = [conversation.view()
                         for conversation in self.conversations]
        roles = [role.serialize() for role in self.roles]
        try:
            wallet = self.wallet.serialize()
        except AttributeError:
            wallet = None
        user = self.__repr__()
        user.update({'roles': roles, 'wallet': wallet,
                     'conversations': conversations, 'boards': boards})
        return user


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


class Role(BaseModel):
    """Role model."""

    id = db.Column(db.Integer(),
                   primary_key=True)
    title = db.Column(db.String(),
                      nullable=False)

    def __repr__(self):
        """Summarized view of a role."""
        return self.serialize()

    def view(self):
        """Detailed view of a role."""
        role = self.serialize()
        role.update({'users': [i.__repr__() for i in self.users]})
        return role
