import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskyBlogger.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'warning'
mail = Mail(app)


# from flaskyBlogger.routes import routes

from flaskyBlogger.main.routes import main
from flaskyBlogger.users.routes import users
from flaskyBlogger.posts.routes import posts

# registering the blueprints
app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(posts)

print(app.config['MAIL_USERNAME'])
print(app.config['MAIL_PASSWORD'])