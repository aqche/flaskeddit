from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from flaskeddit import db
from flaskeddit.models import Community, Post, Reply
from flaskeddit.post import post_blueprint
from flaskeddit.post.forms import PostForm


@post_blueprint.route("/community/<string:name>/post/<string:title>")
def post(name, title):
    page = int(request.args.get("page", 1))
    post = Post.query.filter_by(title=title).first_or_404()
    replies = post.replies.order_by(Reply.date_created.desc()).paginate(
        page=page, per_page=5
    )
    return render_template("post.jinja2", page="recent", post=post, replies=replies)


@post_blueprint.route("/community/<string:name>/post/<string:title>/top")
def top_post(name, title):
    # TODO: Update to sort by most votes?
    page = int(request.args.get("page", 1))
    post = Post.query.filter_by(title=title).first_or_404()
    replies = post.replies.order_by(Reply.date_created.desc()).paginate(
        page=page, per_page=5
    )
    return render_template("post.jinja2", page="top", post=post, replies=replies)


@post_blueprint.route("/community/<string:name>/post/create", methods=["GET", "POST"])
@login_required
def create_post(name):
    community = Community.query.filter_by(name=name).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            post=form.post.data,
            community=community,
            user=current_user,
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
    return "Update Post"


@post_blueprint.route(
    "/community/<string:name>/post/<string:title>/delete", methods=["POST"]
)
@login_required
def delete_post(name, title):
    return "Delete Post"
