from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from flaskeddit import db
from flaskeddit.models import Post, Reply, ReplyVote
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
    "/community/<string:name>/post/<string:title>/reply/<int:reply_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def update_reply(name, title, reply_id):
    reply = Reply.query.get_or_404(reply_id)
    if reply.user_id != current_user.id:
        return redirect(url_for("post.post", name=name, title=title))
    form = ReplyForm()
    if form.validate_on_submit():
        reply.reply = form.reply.data
        db.session.commit()
        flash("Successfully updated reply", "primary")
        return redirect(url_for("post.post", name=name, title=title))
    form.reply.data = reply.reply
    return render_template(
        "update_reply.jinja2", name=name, title=title, reply_id=reply_id, form=form
    )


@reply_blueprint.route(
    "/community/<string:name>/post/<string:title>/reply/<int:reply_id>/delete",
    methods=["POST"],
)
@login_required
def delete_reply(name, title, reply_id):
    reply = Reply.query.get_or_404(reply_id)
    if reply.user_id != current_user.id:
        return redirect(url_for("post.post", name=name, title=title))
    db.session.delete(reply)
    db.session.commit()
    flash("Successfully deleted reply.", "primary")
    return redirect(url_for("post.post", name=name, title=title))


@reply_blueprint.route(
    "/community/<string:name>/post/<string:title>/reply/<int:reply_id>/upvote",
    methods=["POST"],
)
@login_required
def upvote_reply(name, title, reply_id):
    reply = Reply.query.get_or_404(reply_id)
    reply_vote = ReplyVote.query.filter_by(
        user_id=current_user.id, reply_id=reply.id
    ).first()
    if reply_vote is None:
        reply_vote = ReplyVote(vote=1, user_id=current_user.id, reply_id=reply.id)
        db.session.add(reply_vote)
    elif abs(reply_vote.vote) == 1:
        reply_vote.vote = 0
    else:
        reply_vote.vote = 1
    db.session.commit()
    return redirect(request.referrer)


@reply_blueprint.route(
    "/community/<string:name>/post/<string:title>/reply/<int:reply_id>/downvote",
    methods=["POST"],
)
@login_required
def downvote_reply(name, title, reply_id):
    reply = Reply.query.get_or_404(reply_id)
    reply_vote = ReplyVote.query.filter_by(
        user_id=current_user.id, reply_id=reply.id
    ).first()
    if reply_vote is None:
        reply_vote = ReplyVote(vote=-1, user_id=current_user.id, reply_id=reply.id)
        db.session.add(reply_vote)
    elif abs(reply_vote.vote) == 1:
        reply_vote.vote = 0
    else:
        reply_vote.vote = -1
    db.session.commit()
    return redirect(request.referrer)
