from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from flaskeddit import db
from flaskeddit.models import Post, Reply
from flaskeddit.reply import reply_blueprint
from flaskeddit.reply.forms import ReplyForm


@reply_blueprint.route(
    "/community/<string:name>/post/<string:title>/reply", methods=["GET", "POST"]
)
@login_required
def reply(name, title):
    post = Post.query.filter_by(title=title).first_or_404()
    form = ReplyForm()
    if form.validate_on_submit():
        reply = Reply(reply=form.reply.data, post=post, user=current_user)
        db.session.add(reply)
        db.session.commit()
        flash("Successfully created reply", "primary")
        return redirect(url_for("post.post", name=name, title=title))
    return render_template("create_reply.jinja2", name=name, title=title, form=form)


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
