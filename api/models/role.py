"""Role."""

from .base import BaseModel, db


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
