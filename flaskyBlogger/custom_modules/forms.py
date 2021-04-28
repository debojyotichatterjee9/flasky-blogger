from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskyBlogger.models.user_models import User
from flask_login import current_user


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


class AccountUpdateForm(FlaskForm):
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
    avatar = FileField('Avatar',
                        validators=[
                            FileAllowed(['jpg', 'jpeg', 'png']),
                        ])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists!')


class EditPostForm(FlaskForm):
    title = StringField('Title',
                        validators=[
                            DataRequired(),
                            Length(min=2, max=100)
                        ])
    content = TextAreaField('Content',
                        validators=[
                            DataRequired(),
                            Length(min=2, max=1000)
                        ])
    submit = SubmitField('Publish')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user_info = User.query.filter_by(email=email.data).first()
        if user_info is None:
            raise ValidationError('There is no account with the email. Please Register and Login to continue.')



class PasswordResetForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                             ])
    confirm_password = PasswordField('Re-type Password',
                                     validators=[
                                         DataRequired(),
                                         EqualTo('password')
                                     ])
    submit = SubmitField('Reset Password')