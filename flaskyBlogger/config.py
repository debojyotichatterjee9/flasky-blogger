import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "postgres://vemvuchbsdejiu:2ed5608887a83dda65732569f757d343aaefa4788d9e4e9da3154e293a772bd7@ec2-54-196-33-23.compute-1.amazonaws.com:5432/d842aln8tlhs97"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
