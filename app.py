"""
diabetes app:
currently, allows tracking of inventory for consumables
used in day to day treatment of type one diabetes
allows users to define items, use and resupply those items
and view their current inventory
"""
from datetime import datetime

from flask import Flask, jsonify, render_template, request, abort
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

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

    def __init__(self, item_id, quantity):
        self.item_id = item_id
        self.time = datetime.now()
        self.quantity = quantity

    def as_dict(self):
        """
        Method for returning a valid dictionary from SQLAlchemy model objects
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/items', methods=['GET'])
def get_items():
    """
    Returns a JSON document of all items
    """
    return jsonify({'items': list(map(lambda x: x.as_dict(), Item.query.all()))})

@app.route('/items', methods=['POST'])
def add_item():
    """
    For a valid JSON POSt HTTP verb that contains at least
    an item name creates a new item with that name
    """
    if not request.json or not 'name' in request.json:
        abort(400)
    new_item = Item(name=request.json['name'])
    if 'description' in request.json:
        new_item.description = request.json['description']

    db.session.add(new_item)
    db.session.commit()
    return jsonify({'item': new_item.as_dict()}), 201

@app.route('/items/<int:item_id>/inventory', methods=['GET'])
def get_item_inventory(item_id):
    """
    For a given valid item id returns the count on hand

    TODO: Validate item id
    """
    count = sum(transaction.quantity for transaction in Transaction.query.filter_by(item_id=item_id).all())
    return jsonify({"id": item_id, "count": count})


@app.route('/transactions', methods=['GET'])
def get_transactions():
    """
    Returns a JSON document of all transactions
    """
    return jsonify({'transactions': list(map(lambda x: x.as_dict(), Transaction.query.all()))})

@app.route('/transactions', methods=['POST'])
def add_transaction():
    """
    For a valid JSON POST HTTP verb that contains both an item id and a quantity
    creates a new transaction timestamped at now

    TODO: Optionally, take a user specified time
    """
    if not request.json or not 'item_id' in request.json or not 'quantity' in request.json:
        abort(400)
    if Item.query.get(request.json['item_id']) == None:
        abort(400)
    new_transaction = Transaction(item_id=request.json['item_id'], quantity=request.json['quantity'])
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'transaction': new_transaction.as_dict()}), 201

if __name__ == '__main__':
    app.debug = True
    manager.run()
