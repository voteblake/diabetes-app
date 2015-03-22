"""
diabetes app:
currently, allows tracking of inventory for consumables
used in day to day treatment of type one diabetes
allows users to define items, use and resupply those items
and view their current inventory
"""

from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap

from models.database import db

from api.routes import api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
app.register_blueprint(api)

db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

Bootstrap(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    manager.run()
