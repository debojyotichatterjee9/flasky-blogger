from flask import render_template, url_for, redirect, request, Blueprint
from flaskyBlogger.models.post_models import Post
from flask_login import login_user, current_user, login_required


main = Blueprint('main', __name__)


@main.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('./landing/landing.html')


@main.route('/home')
@login_required
def home():
    requested_page = request.args.get('page', 1, type=int)
    list_of_posts = Post.query.order_by(
        Post.date.desc()).paginate(page=requested_page, per_page=2)
    return render_template('./home/home.html', posts=list_of_posts)

# about page


@main.route('/about')
def about():
    return render_template('./about/about.html', title='AboutUs')
