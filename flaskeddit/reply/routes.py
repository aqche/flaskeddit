from flask_login import login_required

from flaskeddit.reply import reply_blueprint


@reply_blueprint.route("/community/<string:name>/post/<string:title>/reply")
@login_required
def reply(name, title):
    return "Create Reply"


@reply_blueprint.route(
    "/community/<string:name>/post/<string:title>/reply/<int:reply_id>/edit"
)
@login_required
def edit_reply(name, title, reply_id):
    return "Edit Reply"


@reply_blueprint.route(
    "/community/<string:name>/post/<string:title>/reply/<int:reply_id>/delete"
)
@login_required
def delete_reply(name, title, reply_id):
    return "Delete Reply"
