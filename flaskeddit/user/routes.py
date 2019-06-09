from flask import render_template

from flaskeddit.models import AppUser
from flaskeddit.user import user_blueprint


@user_blueprint.route("/user/<string:username>")
def app_user(username):
    app_user = AppUser.query.filter_by(username=username).first_or_404()
    return render_template("user.jinja2", app_user=app_user)
