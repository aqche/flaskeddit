from flaskeddit.posts import posts_bp


@posts_bp.route("/")
@posts_bp.route("/posts")
def posts():
    return "Posts"


@posts_bp.route("/posts/top")
def top_posts():
    return "Top Posts"


@posts_bp.route("/posts/user/<int:user_id>")
def user_posts(user_id):
    return "User {0} Posts".format(user_id)
