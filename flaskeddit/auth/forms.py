import re

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length

from flaskeddit.models import AppUser


class RegisterForm(FlaskForm):
    """Form for registering a new user."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", message="Passwords must match."),
            Length(min=6),
        ],
    )
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, username):
        """
        Validates that a user with the given username does not already exist in the
        database.
        """
        app_user = AppUser.query.filter_by(username=username.data.lower()).first()
        if app_user is not None:
            raise ValidationError("Username is taken.")


class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
