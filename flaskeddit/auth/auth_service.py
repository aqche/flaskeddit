from flask_login import login_user, logout_user

from flaskeddit import bcrypt, db
from flaskeddit.models import AppUser


def register_user(username, password):
    """
    Hashes the given password and registers a new user in the database.
    """
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    app_user = AppUser(username=username.lower(), password=hashed_password)
    db.session.add(app_user)
    db.session.commit()


def log_in_user(username, password):
    """
    Hashes and compares the given password with the stored password. If it is a match,
    logs a user in.
    """
    app_user = AppUser.query.filter_by(username=username.lower()).first()
    if app_user and bcrypt.check_password_hash(app_user.password, password):
        login_user(app_user)
        return True
    else:
        return False


def log_out_user():
    """
    Logs the current user out.
    """
    logout_user()
