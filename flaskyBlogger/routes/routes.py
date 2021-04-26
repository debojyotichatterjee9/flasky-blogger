import secrets
import os
from flaskyBlogger import app, db, bcrypt
from flask import render_template, url_for, redirect, flash, request
from flaskyBlogger.custom_modules.forms import RegistrationForm, LoginForm, AccountUpdateForm
from flaskyBlogger.models.user_models import User
from flaskyBlogger.models.post_models import Post
from flask_login import login_user, current_user, login_required, logout_user


dummy_data = [
    {
        'author': 'John Lee',
        'title': 'A Beautiful World',
        'content': 'This is a sample data to fill in the void.',
        'date': '01 April 2021'
    },
    {
        'author': 'Mary Williams',
        'title': 'Woman Power',
        'content': 'Women are the secret power to the society.',
        'date': '05 April 2020'
    }
]

# home page


@app.route('/')
@app.route('/home')
def home():
    return render_template('./home/home.html', data=dummy_data)

# about page


@app.route('/about')
def about():
    return render_template('./about/about.html', title='AboutUs')


@app.route('/register', methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():

        # encrypting the password before storing
        hashed_password = bcrypt.generate_password_hash(reg_form.confirm_password.data).decode("utf-8")
        
        # creating the user instance from the data recieved
        user = User(
            first_name = reg_form.first_name.data,
            last_name = reg_form.last_name.data,
            username = reg_form.username.data,
            email = reg_form.email.data,
            password = hashed_password)

        # saving the user to the databse
        db.session.add(user)
        db.session.commit()

        flash(f'Account created successfully! Please Login to continue.', 'success')
        return redirect(url_for('login'))
    return render_template('./register/register.html', title='Registration', form=reg_form)


@app.route('/login', methods=["GET", "POST"])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)

            # checking if a param exists for a existing secured page in the application
            next_page = request.args.get('next')

            flash(f'Welcome {login_form.email.data}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Please check the email or password!', 'danger')
    return render_template('./login/login.html', title='Login', form=login_form)


@app.route('/logout', methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('login'))


def upload_avatar(image_data):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(image_data.filename)
    file_name = random_hex + file_ext
    avatar_path = os.path.join(app.root_path, "static/images/avatars", file_name)
    print(avatar_path)
    image_data.save(avatar_path)
    return avatar_path

@app.route('/user-account', methods=["GET", "POST"])
@login_required
def user_account():
    user_avatar = url_for('static',filename='images/avatars/' + current_user.avatar)
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
        return redirect(url_for('user_account'))
    elif request.method == "GET":
        account_update_form.first_name.data = current_user.first_name
        account_update_form.last_name.data = current_user.last_name
        account_update_form.username.data = current_user.username
        account_update_form.email.data = current_user.email
    return render_template('./user_account/user_account.html', title='User Account', avatar=user_avatar, form=account_update_form)