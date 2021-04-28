from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

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
