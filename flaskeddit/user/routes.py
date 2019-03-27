from flaskeddit.user import user_blueprint


@user_blueprint.route("/user/<int:user_id>")
def user(user_id):
    return "User Profile"


@user_blueprint.route("/user/<int:user_id>/posts")
def user_posts(user_id):
    return "User Posts"


@user_blueprint.route("/user/<int:user_id>/replies")
def user_replies(user_id):
    return "User Replies"


@user_blueprint.route("/user/<int:user_id>/subscriptions")
def user_subscriptions(user_id):
    return "User Subscriptions"


@user_blueprint.route("/user/<int:user_id>/communities")
def user_communities(user_id):
    return "User Communities"
