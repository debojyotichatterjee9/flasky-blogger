from flaskyBlogger import app, db, bcrypt, mail
from flask import render_template, url_for, redirect, flash, request, Blueprint
from flaskyBlogger.users.forms import (RegistrationForm, LoginForm, AccountUpdateForm, 
                                                PasswordResetRequestForm, PasswordResetForm)
from flaskyBlogger.models.user_models import User
from flaskyBlogger.models.post_models import Post
from flask_login import login_user, current_user, login_required, logout_user
from flaskyBlogger.users.helpers import upload_avatar, send_reset_req_email


users = Blueprint('users', __name__)


@users.route('/register', methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():

        # encrypting the password before storing
        hashed_password = bcrypt.generate_password_hash(
            reg_form.confirm_password.data).decode("utf-8")

        # creating the user instance from the data recieved
        user = User(
            first_name=reg_form.first_name.data,
            last_name=reg_form.last_name.data,
            username=reg_form.username.data,
            email=reg_form.email.data,
            password=hashed_password)

        # saving the user to the databse
        db.session.add(user)
        db.session.commit()

        flash(f'Account created successfully! Please Login to continue.', 'success')
        return redirect(url_for('users.login'))
    return render_template('./register/register.html', title='Registration', form=reg_form)


@users.route('/login', methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)

            # checking if a param exists for a existing secured page in the application
            next_page = request.args.get('next')

            flash(f'Welcome {current_user.first_name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Please check the email or password!', 'danger')
    return render_template('./login/login.html', title='Login', form=login_form)


@users.route('/logout', methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/user-account', methods=["GET", "POST"])
@login_required
def user_account():
    account_update_form = AccountUpdateForm()
    if account_update_form.validate_on_submit():
        if account_update_form.avatar.data:
            avatar_file = upload_avatar(account_update_form.avatar.data)
            current_user.avatar = avatar_file
        current_user.first_name = account_update_form.first_name.data
        current_user.last_name = account_update_form.last_name.data
        current_user.username = account_update_form.username.data
        current_user.email = account_update_form.email.data
        db.session.commit()
        flash('Updated sucessfully!', 'success')
        return redirect(url_for('users.user_account'))
    elif request.method == "GET":
        account_update_form.first_name.data = current_user.first_name
        account_update_form.last_name.data = current_user.last_name
        account_update_form.username.data = current_user.username
        account_update_form.email.data = current_user.email
    user_avatar = url_for(
        'static', filename='images/avatars/' + current_user.avatar)
    return render_template('./user_account/user_account.html', title='User Account', avatar=user_avatar, form=account_update_form)


@users.route('/posts/<string:username>')
@login_required
def user_posts(username):
    requested_page = request.args.get('page', 1, type=int)
    user_info = User.query.filter_by(username=username).first_or_404()
    list_of_posts = Post.query.filter_by(author=user_info).\
        order_by(Post.date.desc()).\
        paginate(page=requested_page, per_page=2)
    return render_template('./post/user_posts.html', title=f"{user_info.first_name}'s Posts", posts=list_of_posts, user=user_info)





@users.route('/reset-request', methods=["GET", "POST"])
def reset_request():
    #  redirect to home if logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    password_reset_form = PasswordResetRequestForm()

    if password_reset_form.validate_on_submit():
        user_info = User.query.filter_by(
            email=password_reset_form.email.data).first()
        send_reset_req_email(user_info)
        flash("An email has been sent for password reset with instructions.", "info")
        return redirect(url_for("users.login"))
    return render_template('./user_account/password_reset_request.html', title="Reset Request", form=password_reset_form)


@users.route('/reset-password/<string:token>', methods=["GET", "POST"])
def reset_password(token):
    #  redirect to home if logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # validating the user
    user_info = User.validate_token(token)

    if user_info is None:
        flash('Invalid or expired token!', 'warning')
        return redirect(url_for('users.reset_request'))

    password_reset_form = PasswordResetForm()

    if password_reset_form.validate_on_submit():

        # encrypting the password before storing
        hashed_password = bcrypt.generate_password_hash(
            password_reset_form.confirm_password.data).decode("utf-8")

        # saving the user to the databse
        user_info.password = hashed_password
        db.session.commit()

        flash(f'Password updated successfully! Please Login to continue.', 'success')
        return redirect(url_for('users.login'))

    return render_template('./user_account/password_reset.html', title="Reset Password", form=password_reset_form)
