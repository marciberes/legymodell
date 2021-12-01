from . import db
from flask_login import UserMixin

class Ad(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.String(15))
    address = db.Column(db.String(50))
    contact = db.Column(db.String(100))
    adtype = db.Column(db.String(20))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    ads = db.relationship('Ad')