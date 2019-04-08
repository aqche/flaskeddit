from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ReplyForm(FlaskForm):
    reply = TextAreaField("Reply", validators=[DataRequired()])
    submit = SubmitField("Submit")
