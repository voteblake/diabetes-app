from datetime import datetime

from flask import Flask, jsonify, request, abort
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
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    transactions = db.relationship("Transaction", backref = "item")

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Item %r>' % self.name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key = True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    time = db.Column(db.DateTime)
    quantity = db.Column(db.Integer)

    def __init__(self, item_id, quantity):
        self.item_id = item_id
        self.time = datetime.now()
        self.quantity = quantity

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({'items': list(map(lambda x: x.as_dict(), Item.query.all()))})

@app.route('/transactions', methods=['GET'])
def get_transactions():
    return jsonify({'transactions': list(map(lambda x: x.as_dict(), Transaction.query.all()))})

@app.route('/transactions', methods=['POST'])
def add_transaction():
    if not request.json or not 'item_id' in request.json or not 'quantity' in request.json:
        abort(400)
    new_transaction = Transaction(item_id = request.json['item_id'], quantity = request.json['quantity'])
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'transaction': new_transaction.as_dict()}), 201

if __name__ == '__main__':
    app.debug = True
    manager.run()
