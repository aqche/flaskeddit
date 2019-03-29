import re

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length

from flaskeddit.models import User


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", message="Passwords must match."),
            Length(min=8, message="Password should be at least 8 characters long."),
        ],
    )
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken.")

    def validate_password(self, password):
        if re.search("\d", password.data) is None:
            raise ValidationError("Password should contain at least 1 number.")
        elif re.search("[A-Z]", password.data) is None:
            raise ValidationError(
                "Password should contain at least 1 uppercase character."
            )
        elif re.search("[a-z]", password.data) is None:
            raise ValidationError(
                "Password should contain at least 1 lowercase character."
            )
        elif re.search("\W", password.data) is None:
            raise ValidationError(
                "Password should contain at least 1 special character."
            )


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
