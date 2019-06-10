from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from flaskeddit import db
from flaskeddit.models import AppUser, Community, Post, PostVote, Reply, ReplyVote
from flaskeddit.post import post_blueprint
from flaskeddit.post.forms import PostForm, UpdatePostForm


@post_blueprint.route("/community/<string:name>/post/<string:title>")
def post(name, title):
    page = int(request.args.get("page", 1))
    post = (
        db.session.query(
            Post.id,
            Post.title,
            Post.post,
            Post.date_created,
            Post.user_id,
            db.func.coalesce(db.func.sum(PostVote.vote), 0).label("votes"),
            AppUser.username,
            Community.name.label("community_name"),
            Community.description.label("community_description"),
        )
        .join(AppUser, Post.user_id == AppUser.id)
        .join(Community, Post.community_id == Community.id)
        .outerjoin(PostVote, Post.id == PostVote.post_id)
        .filter(Post.title == title)
        .filter(Community.name == name)
        .group_by(Post.id, AppUser.id, Community.id)
        .first_or_404()
    )
    replies = (
        db.session.query(
            Reply.id,
            Reply.reply,
            Reply.user_id,
            Reply.date_created,
            db.func.coalesce(db.func.sum(ReplyVote.vote), 0).label("votes"),
            AppUser.username,
        )
        .join(AppUser, Reply.user_id == AppUser.id)
        .outerjoin(ReplyVote, Reply.id == ReplyVote.reply_id)
        .filter(Reply.post_id == post.id)
        .group_by(Reply.id, AppUser.id)
        .order_by(Reply.date_created.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("post.jinja2", page="recent", post=post, replies=replies)


@post_blueprint.route("/community/<string:name>/post/<string:title>/top")
def top_post(name, title):
    page = int(request.args.get("page", 1))
    post = (
        db.session.query(
            Post.id,
            Post.title,
            Post.post,
            Post.date_created,
            Post.user_id,
            db.func.coalesce(db.func.sum(PostVote.vote), 0).label("votes"),
            AppUser.username,
            Community.name.label("community_name"),
            Community.description.label("community_description"),
        )
        .join(AppUser, Post.user_id == AppUser.id)
        .join(Community, Post.community_id == Community.id)
        .outerjoin(PostVote, Post.id == PostVote.post_id)
        .filter(Post.title == title)
        .filter(Community.name == name)
        .group_by(Post.id, AppUser.id, Community.id)
        .first_or_404()
    )
    replies = (
        db.session.query(
            Reply.id,
            Reply.reply,
            Reply.user_id,
            Reply.date_created,
            db.func.coalesce(db.func.sum(ReplyVote.vote), 0).label("votes"),
            AppUser.username,
        )
        .join(AppUser, Reply.user_id == AppUser.id)
        .outerjoin(ReplyVote, Reply.id == ReplyVote.reply_id)
        .filter(Reply.post_id == post.id)
        .group_by(Reply.id, AppUser.id)
        .order_by(db.literal_column("votes").desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("post.jinja2", page="top", post=post, replies=replies)


@post_blueprint.route("/community/<string:name>/post/create", methods=["GET", "POST"])
@login_required
def create_post(name):
    community = Community.query.filter_by(name=name).first_or_404()
    form = PostForm()
    form.community_id.data = community.id
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            post=form.post.data,
            community=community,
            app_user=current_user,
        )
        db.session.add(post)
        db.session.commit()
        flash("Successfully created post.", "primary")
        return redirect(url_for("post.post", name=name, title=post.title))
    return render_template("create_post.jinja2", name=name, form=form)


@post_blueprint.route(
    "/community/<string:name>/post/<string:title>/update", methods=["GET", "POST"]
)
@login_required
def update_post(name, title):
    post = (
        db.session.query(Post)
        .join(Community, Post.community_id == Community.id)
        .filter(Post.title == title)
        .filter(Community.name == name)
        .first_or_404()
    )
    if post.user_id != current_user.id:
        return redirect(url_for("post.post", name=name, title=title))
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.post = form.post.data
        db.session.commit()
        flash("Successfully updated post.", "primary")
        return redirect(url_for("post.post", name=name, title=title))
    form.post.data = post.post
    return render_template("update_post.jinja2", name=name, title=title, form=form)


@post_blueprint.route(
    "/community/<string:name>/post/<string:title>/delete", methods=["POST"]
)
@login_required
def delete_post(name, title):
    post = (
        db.session.query(Post)
        .join(Community, Post.community_id == Community.id)
        .filter(Post.title == title)
        .filter(Community.name == name)
        .first_or_404()
    )
    if post.user_id != current_user.id:
        return redirect(url_for("post.post", name=name, title=title))
    db.session.delete(post)
    db.session.commit()
    flash("Successfully deleted post.", "primary")
    return redirect(url_for("community.community", name=name))


@post_blueprint.route(
    "/community/<string:name>/post/<string:title>/upvote", methods=["POST"]
)
@login_required
def upvote_post(name, title):
    post = (
        db.session.query(Post)
        .join(Community, Post.community_id == Community.id)
        .filter(Post.title == title)
        .filter(Community.name == name)
        .first_or_404()
    )
    post_vote = PostVote.query.filter_by(
        user_id=current_user.id, post_id=post.id
    ).first()
    if post_vote is None:
        post_vote = PostVote(vote=1, user_id=current_user.id, post_id=post.id)
        db.session.add(post_vote)
    elif abs(post_vote.vote) == 1:
        post_vote.vote = 0
    else:
        post_vote.vote = 1
    db.session.commit()
    return redirect(request.referrer)


@post_blueprint.route(
    "/community/<string:name>/post/<string:title>/downvote", methods=["POST"]
)
@login_required
def downvote_post(name, title):
    post = (
        db.session.query(Post)
        .join(Community, Post.community_id == Community.id)
        .filter(Post.title == title)
        .filter(Community.name == name)
        .first_or_404()
    )
    post_vote = PostVote.query.filter_by(
        user_id=current_user.id, post_id=post.id
    ).first()
    if post_vote is None:
        post_vote = PostVote(vote=-1, user_id=current_user.id, post_id=post.id)
        db.session.add(post_vote)
    elif abs(post_vote.vote) == 1:
        post_vote.vote = 0
    else:
        post_vote.vote = -1
    db.session.commit()
    return redirect(request.referrer)
