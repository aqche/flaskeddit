from flask_login import login_required

from flaskeddit.reply import reply_blueprint


@reply_blueprint.route("/community/<int:community_id>/post/<int:post_id>/reply")
@login_required
def reply(community_id, post_id):
    return "Create Reply"


@reply_blueprint.route(
    "/community/<int:community_id>/post/<int:post_id>/reply/<int:reply_id>/edit"
)
@login_required
def edit_reply(community_id, post_id, reply_id):
    return "Edit Reply"


@reply_blueprint.route(
    "/community/<int:community_id>/post/<int:post_id>/reply/<int:reply_id>/delete"
)
@login_required
def delete_reply(community_id, post_id, reply_id):
    return "Delete Reply"
