from flask_login import login_required

from flaskeddit.post import post_blueprint


@post_blueprint.route("/community/<int:community_id>/post/<int:post_id>")
def post(community_id, post_id):
    return "View Post"


@post_blueprint.route("/community/<int:community_id>/post/create")
@login_required
def create_post(community_id):
    return "Create Post"


@post_blueprint.route("/community/<int:community_id>/post/<int:post_id>/update")
@login_required
def update_post(community_id, post_id):
    return "Update Post"


@post_blueprint.route("/community/<int:community_id>/post/<int:post_id>/delete")
@login_required
def delete_post(community_id, post_id):
    return "Delete Post"
