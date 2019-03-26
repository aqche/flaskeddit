from flask_login import login_required

from flaskeddit.posts import posts_blueprint


@posts_blueprint.route("/")
@posts_blueprint.route("/posts")
@login_required
def posts():
    return "Posts"


@posts_blueprint.route("/posts/top")
@login_required
def top_posts():
    return "Top Posts"


@posts_blueprint.route("/posts/user/<int:user_id>")
@login_required
def user_posts(user_id):
    return "User {0} Posts".format(user_id)
