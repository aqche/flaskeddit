from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    post = TextAreaField("Post", validators=[DataRequired()])
    submit = SubmitField("Create")


class UpdatePostForm(FlaskForm):
    post = TextAreaField("Post", validators=[DataRequired()])
    submit = SubmitField("Create")
