import re

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo

from flaskeddit.models import AppUser


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", message="Passwords must match."),
        ],
    )
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, username):
        app_user = AppUser.query.filter_by(username=username.data.lower()).first()
        if app_user is not None:
            raise ValidationError("Username is taken.")

    def validate_password(self, password):
        if (
            re.search(r"\d", password.data) is None
            or re.search(r"[A-Z]", password.data) is None
            or re.search(r"[a-z]", password.data) is None
            or re.search(r"\W", password.data) is None
            or len(password.data) < 8
        ):
            raise ValidationError(
                "Password should be at least 8 characters long including a number, an uppercase character, a lowercase character, and a special character."
            )


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
