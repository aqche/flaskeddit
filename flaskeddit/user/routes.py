from flask import render_template

from flaskeddit.user import user_blueprint, user_service


@user_blueprint.route("/user/<string:username>")
def app_user(username):
    """
    Route displaying a user's profile page.
    """
    user = user_service.get_user(username)
    return render_template("user.jinja2", app_user=user)
