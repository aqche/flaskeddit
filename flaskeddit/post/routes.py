from flask_login import login_required

from flaskeddit.post import post_blueprint


@post_blueprint.route("/post/<int:post_id>")
@login_required
def post(post_id):
    return "Post: {0}".format(post_id)


@post_blueprint.route("/post/create")
@login_required
def create_post():
    return "Create Post"


@post_blueprint.route("/post/update/<int:post_id>")
@login_required
def update_post(post_id):
    return "Update Post: {0}".format(post_id)


@post_blueprint.route("/post/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    return "Delete Post: {0}".format(post_id)
