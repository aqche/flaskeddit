from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from flaskeddit import db
from flaskeddit.community import community_blueprint
from flaskeddit.community.forms import CommunityForm, UpdateCommunityForm
from flaskeddit.models import Community, Post, PostVote, User


@community_blueprint.route("/community/<string:name>")
def community(name):
    page = int(request.args.get("page", 1))
    community = db.session.query(Community).filter_by(name=name).first_or_404()
    posts_without_votes = db.session.query(Post, db.literal(0).label("votes")).filter(
        Post.community_id == community.id
    )
    posts_with_votes = (
        db.session.query(Post, db.func.sum(PostVote.vote).label("votes"))
        .join(PostVote, Post.id == PostVote.post_id)
        .filter(Post.community_id == community.id)
        .group_by(Post.id)
    )
    posts_union = posts_without_votes.union_all(posts_with_votes).subquery()
    posts = (
        db.session.query(
            posts_union.c.post_title.label("title"),
            posts_union.c.post_post.label("post"),
            posts_union.c.post_date_created.label("date_created"),
            db.func.sum(posts_union.c.votes).label("votes"),
            User.username,
        )
        .join(posts_union, posts_union.c.post_user_id == User.id)
        .group_by(posts_union.c.post_id)
        .order_by(posts_union.c.post_date_created.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template(
        "community.jinja2", page="recent", community=community, posts=posts
    )


@community_blueprint.route("/community/<string:name>/top")
def top_community(name):
    page = int(request.args.get("page", 1))
    community = db.session.query(Community).filter_by(name=name).first_or_404()
    posts_without_votes = db.session.query(Post, db.literal(0).label("votes")).filter(
        Post.community_id == community.id
    )
    posts_with_votes = (
        db.session.query(Post, db.func.sum(PostVote.vote).label("votes"))
        .join(PostVote, Post.id == PostVote.post_id)
        .filter(Post.community_id == community.id)
        .group_by(Post.id)
    )
    posts_union = posts_without_votes.union_all(posts_with_votes).subquery()
    posts = (
        db.session.query(
            posts_union.c.post_title.label("title"),
            posts_union.c.post_post.label("post"),
            posts_union.c.post_date_created.label("date_created"),
            db.func.sum(posts_union.c.votes).label("votes"),
            User.username,
        )
        .join(posts_union, posts_union.c.post_user_id == User.id)
        .group_by(posts_union.c.post_id)
        .order_by(db.literal_column("votes").desc())
        .paginate(page=page, per_page=5)
    )
    return render_template(
        "community.jinja2", page="top", community=community, posts=posts
    )


@community_blueprint.route("/community/create", methods=["GET", "POST"])
@login_required
def create_community():
    form = CommunityForm()
    if form.validate_on_submit():
        community = Community(
            name=form.name.data, description=form.description.data, user=current_user
        )
        db.session.add(community)
        db.session.commit()
        flash("Successfully created community.", "primary")
        return redirect(url_for("community.community", name=community.name))
    return render_template("create_community.jinja2", form=form)


@community_blueprint.route("/community/<string:name>/update", methods=["GET", "POST"])
@login_required
def update_community(name):
    community = Community.query.filter_by(name=name).first_or_404()
    if community.user_id != current_user.id:
        return redirect(url_for("community.community", name=name))
    form = UpdateCommunityForm()
    if form.validate_on_submit():
        community.description = form.description.data
        db.session.commit()
        flash("Successfully updated community.", "primary")
        return redirect(url_for("community.community", name=name))
    form.description.data = community.description
    return render_template("update_community.jinja2", name=name, form=form)


@community_blueprint.route("/community/<string:name>/delete", methods=["POST"])
@login_required
def delete_community(name):
    community = Community.query.filter_by(name=name).first_or_404()
    if community.user_id != current_user.id:
        return redirect(url_for("community.community", name=name))
    db.session.delete(community)
    db.session.commit()
    flash("Successfully deleted community.", "primary")
    return redirect(url_for("feed.feed"))
