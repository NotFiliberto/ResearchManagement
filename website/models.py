# going to use it as a sort of database models

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):  # User class extends db.Model and UserMixin
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    # relationship must be written with CAPITAL LETTER (we do not know why)
    notes = db.relationship('Note')


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # foreign keys must be LOWER CASE
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))