import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskyBlogger.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'warning'
mail = Mail()


# from flaskyBlogger.routes import routes
from flaskyBlogger.main.routes import main
from flaskyBlogger.users.routes import users
from flaskyBlogger.posts.routes import posts

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    print(app.config['MAIL_USERNAME'])
    print(app.config['MAIL_PASSWORD'])
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    # registering the blueprints
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)

    return app