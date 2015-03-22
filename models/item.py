from .database import db

class Item(db.Model):
    """
    Item class - SQLAlchemy Model - Defines an instance
    of items, consumable objects whose inventory the user
    wishes to track.
    """
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    transactions = db.relationship("Transaction", backref="item")

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Item %r>' % self.name

    def as_dict(self):
        """
        Method for returning a valid dictionary from SQLAlchemy model objects
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
