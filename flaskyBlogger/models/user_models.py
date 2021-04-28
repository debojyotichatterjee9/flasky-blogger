from flask import current_app
from flaskyBlogger import db, login_manager
from datetime import datetime
from flask_login import UserMixin

from itsdangerous import TimedJSONWebSignatureSerializer as TJSONSerializer



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    avatar = db.Column(db.String(20), nullable=False, default='default_avatar.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def generate_token(self, exp_in_secs=1800):
        s = TJSONSerializer(current_app.config['SECRET_KEY'], exp_in_secs)
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        return token

    @staticmethod
    def validate_token(token):
        s = TJSONSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # dunder method or called magic method
    def __repr__(self):
        return f"User('{self.first_name}, {self.last_name}, {self.username}', '{self.email}', '{self.avatar}')"