from __init__ import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class note_info(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    DATA = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey('user_info.id'))

class user_info(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    EMAIL = db.Column(db.String(50), nullable=False, unique=True)
    USERNAME = db.Column(db.String(50), nullable=False, unique=True)
    PASSWORD = db.Column(db.String(200), nullable=False)
    NOTES = db.relationship('note_info')
