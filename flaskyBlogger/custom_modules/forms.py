from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskyBlogger.models.user_models import User


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[
                                 DataRequired(),
                                 Length(min=2, max=20)
                             ])
    last_name = StringField('Last Name',
                            validators=[
                                DataRequired(),
                                Length(min=2, max=20)
                            ])
    username = StringField('Username',
                           validators=[
                               DataRequired(),
                               Length(min=2, max=20)
                           ])
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                             ])
    confirm_password = PasswordField('Re-type Password',
                                     validators=[
                                         DataRequired(),
                                         EqualTo('password')
                                     ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists!')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                             ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
