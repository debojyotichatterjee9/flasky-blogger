import os
import secrets
from PIL import Image
from flask import current_app
from flaskyBlogger import mail
from flask import url_for
from flask_mail import Message

def upload_avatar(image_data):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(image_data.filename)
    file_name = random_hex + file_ext
    avatar_path = os.path.join(
        current_app.root_path, "static/images/avatars", file_name)

    # resizing image
    output_size = (125, 125)
    i = Image.open(image_data)
    i.thumbnail(output_size)

    i.save(avatar_path)
    return file_name


def send_reset_req_email(user_info):
    token = user_info.generate_token()
    message = Message('Password Reset Request',
                      sender='support@flaskyblogger.com',
                      recipients=[user_info.email])
    message.body = f'''To reset your password, please visit the following link:
{url_for("users.reset_password", token=token, _external=True)}

If you did not send this request, please ignore the mail and no changes will be made.
'''
    mail.send(message)
