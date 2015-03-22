from datetime import datetime

from .database import db

class Transaction(db.Model):
    """
    Transaction class - SQLAlchemy Model - A transaction is an Integer
    quantity change in the count on hand of any one given item. The aggregate of
    these is used to calculate quantity on hand.
    """
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    time = db.Column(db.DateTime)
    quantity = db.Column(db.Integer)
    adjustment = db.Column(db.Boolean)

    def __init__(self, item_id, quantity, adjustment=False):
        self.item_id = item_id
        self.time = datetime.utcnow()
        self.quantity = quantity
        self.adjustment = adjustment

    def as_dict(self):
        """
        Method for returning a valid dictionary from SQLAlchemy model objects
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
