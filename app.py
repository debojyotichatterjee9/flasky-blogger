from flask import Flask, escape, request, render_template, url_for, redirect, flash
from custom_modules.forms import RegistrationForm, LoginForm

app = Flask(__name__)

# secret key for the application
app.config['SECRET_KEY'] = 'afe5ae8b579a863afb52b97354a1c9c649e3055fbf5165d127b29650ad904ee5'

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
        flash(f'Account created successfully for {reg_form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('./register/register.html', title='Registration', form=reg_form)

@app.route('/login')
def login():
    login_form = LoginForm()
    return render_template('./login/login.html', title='Login', form=login_form)

# if running this file directly using python then the below condition is true
if __name__ == '__main__':
    app.run(debug=True)
