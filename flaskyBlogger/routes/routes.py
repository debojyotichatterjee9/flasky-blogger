from flaskyBlogger import app
from flask import render_template, url_for, redirect, flash
from flaskyBlogger.custom_modules.forms import RegistrationForm, LoginForm
from flaskyBlogger.models.user_models import User
from flaskyBlogger.models.post_models import Post


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
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        flash(
            f'Account created successfully for {reg_form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('./register/register.html', title='Registration', form=reg_form)


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == 'admin@admin.com' and login_form.password.data == 'password':
            flash(f'Welcome {login_form.email.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Please check the email or password!', 'danger')
    return render_template('./login/login.html', title='Login', form=login_form)
