"""User."""

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
