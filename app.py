"""
diabetes app:
currently, allows tracking of inventory for consumables
used in day to day treatment of type one diabetes
allows users to define items, use and resupply those items
and view their current inventory
"""

from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap

from models.database import db

from api.routes import api
from spa.routes import spa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
app.register_blueprint(api)
app.register_blueprint(spa)

db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

Bootstrap(app)

if __name__ == '__main__':
    app.debug = True
    manager.run()
