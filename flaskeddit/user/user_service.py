from flaskeddit.models import AppUser


def get_user(username):
    """Gets a user."""
    user = AppUser.query.filter_by(username=username).first()
    return user
