from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import click
from flask.cli import with_appcontext

db = SQLAlchemy()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)
    user = relationship(User)
    created = db.Column(db.DateTime, default=datetime.now())
    contact_name = db.Column(db.String(30), nullable=False)
    contact_number = db.Column(db.Integer, nullable=False)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')

def init_db(app):
    app.cli.add_command(init_db_command)
