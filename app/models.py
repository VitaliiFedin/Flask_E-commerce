from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash_password = db.Column(db.String(128))
    profile = db.Column(db.String(120), unique=False, nullable=False, default='profile.jpg')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute')

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


