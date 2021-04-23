from flaskyBlogger import app, db, bcrypt
from flask import render_template, url_for, redirect, flash
from flaskyBlogger.custom_modules.forms import RegistrationForm, LoginForm
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
            flash(f'Welcome {login_form.email.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Please check the email or password!', 'danger')
    return render_template('./login/login.html', title='Login', form=login_form)


@app.route('/logout', methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user-account', methods=["GET"])
@login_required
def user_account():
    return render_template('./user_account/user_account.html', title='User Account')