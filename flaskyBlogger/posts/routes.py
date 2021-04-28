from flaskyBlogger import db
from flask import render_template, url_for, redirect, flash, request, abort, Blueprint
from flaskyBlogger.posts.forms import EditPostForm
from flaskyBlogger.models.post_models import Post
from flask_login import current_user, login_required


posts = Blueprint('posts', __name__)


@posts.route('/post/create-post', methods=["GET", "POST"])
@login_required
def create_post():
    create_post_form = EditPostForm()
    if create_post_form.validate_on_submit():
        new_post = Post(title=create_post_form.title.data,
                        content=create_post_form.content.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Published successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('./post/edit_post.html', title='New Post', form=create_post_form, legend="Create a new post")


@posts.route('/post/<int:post_id>', methods=["GET", "POST"])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('./post/post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    update_post_form = EditPostForm()
    if update_post_form.validate_on_submit():
        post.title = update_post_form.title.data
        post.content = update_post_form.content.data
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == "GET":
        update_post_form.title.data = post.title
        update_post_form.content.data = post.content
    return render_template('./post/edit_post.html', title=post.title, post=post, form=update_post_form, legend="Edit your post")


@posts.route('/post/<int:post_id>/delete', methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'{post.title} deleted successfully!', 'danger')
    return redirect(url_for('main.home'))
