from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# secret key for the application
app.config['SECRET_KEY'] = 'afe5ae8b579a863afb52b97354a1c9c649e3055fbf5165d127b29650ad904ee5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

from flaskyBlogger.routes import routes