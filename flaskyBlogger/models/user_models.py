from flaskyBlogger import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    avatar = db.Column(db.String(20), nullable=False, default='default_avatar.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    # dunder method or magic method
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.avatar}')"