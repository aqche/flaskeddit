from flask import render_template

from flaskeddit.models import User
from flaskeddit.user import user_blueprint


@user_blueprint.route("/user/<string:username>")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.jinja2", user=user)
