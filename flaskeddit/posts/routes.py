from flaskeddit.posts import posts_blueprint


@posts_blueprint.route("/")
@posts_blueprint.route("/posts")
def posts():
    return "Posts"


@posts_blueprint.route("/posts/top")
def top_posts():
    return "Top Posts"


@posts_blueprint.route("/posts/user/<int:user_id>")
def user_posts(user_id):
    return "User {0} Posts".format(user_id)
