"""
diabetes app:
currently, allows tracking of inventory for consumables
used in day to day treatment of type one diabetes
allows users to define items, use and resupply those items
and view their current inventory
"""

from flask import Flask, jsonify, render_template, request, abort
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap

from models.database import db
from models.item import Item
from models.transaction import Transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'

db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

Bootstrap(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/items', methods=['GET'])
def get_items():
    """
    Returns a JSON document of all items
    """
    return jsonify(items=list(map(lambda x: x.as_dict(), Item.query.all())))

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
    return jsonify(item=new_item.as_dict()), 201

@app.route('/items/<int:item_id>/inventory', methods=['GET'])
def get_item_inventory(item_id):
    """
    For a given valid item id returns the count on hand
    """
    Item.query.get_or_404(item_id)
    count = sum(transaction.quantity for transaction in Transaction.query.filter_by(item_id=item_id).all())
    return jsonify({"item":{"id": item_id, "count": count}})


@app.route('/transactions', methods=['GET'])
def get_transactions():
    """
    Returns a JSON document of all transactions
    """
    return jsonify(transactions=list(map(lambda x: x.as_dict(), Transaction.query.all())))

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
    if 'adjustment' in request.json:
        new_transaction.adjustment = request.json['adjustment']
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify(transaction=new_transaction.as_dict()), 201

if __name__ == '__main__':
    app.debug = True
    manager.run()
