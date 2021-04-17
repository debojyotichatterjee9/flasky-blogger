from flask import Flask, escape, request, render_template

app = Flask(__name__)

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

# if running this file directly using python then the below condition is true
if __name__ == '__main__':
    app.run(debug=True)