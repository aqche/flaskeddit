from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from flaskeddit import db
from flaskeddit.community import community_blueprint
from flaskeddit.community.forms import CommunityForm, UpdateCommunityForm
from flaskeddit.models import AppUser, Community, CommunityMember, Post, PostVote


@community_blueprint.route("/community/<string:name>")
def community(name):
    page = int(request.args.get("page", 1))
    community = Community.query.filter_by(name=name).first_or_404()
    posts = (
        db.session.query(
            Post.title,
            Post.post,
            Post.date_created,
            db.func.coalesce(db.func.sum(PostVote.vote), 0).label("votes"),
            AppUser.username,
        )
        .outerjoin(PostVote, Post.id == PostVote.post_id)
        .join(AppUser, Post.user_id == AppUser.id)
        .filter(Post.community_id == community.id)
        .group_by(Post.id)
        .order_by(Post.date_created.desc())
        .paginate(page=page, per_page=5)
    )
    if current_user.is_authenticated:
        community_member = CommunityMember.query.filter_by(
            community_id=community.id, user_id=current_user.id
        ).first()
    else:
        community_member = None
    return render_template(
        "community.jinja2",
        page="recent",
        community=community,
        posts=posts,
        community_member=community_member,
    )


@community_blueprint.route("/community/<string:name>/top")
def top_community(name):
    page = int(request.args.get("page", 1))
    community = Community.query.filter_by(name=name).first_or_404()
    posts = (
        db.session.query(
            Post.title,
            Post.post,
            Post.date_created,
            db.func.coalesce(db.func.sum(PostVote.vote), 0).label("votes"),
            AppUser.username,
        )
        .outerjoin(PostVote, Post.id == PostVote.post_id)
        .join(AppUser, Post.user_id == AppUser.id)
        .filter(Post.community_id == community.id)
        .group_by(Post.id)
        .order_by(db.literal_column("votes").desc())
        .paginate(page=page, per_page=5)
    )
    if current_user.is_authenticated:
        community_member = CommunityMember.query.filter_by(
            community_id=community.id, user_id=current_user.id
        ).first()
    else:
        community_member = None
    return render_template(
        "community.jinja2",
        page="top",
        community=community,
        posts=posts,
        community_member=community_member,
    )


@community_blueprint.route("/community/create", methods=["GET", "POST"])
@login_required
def create_community():
    form = CommunityForm()
    if form.validate_on_submit():
        community = Community(
            name=form.name.data,
            description=form.description.data,
            app_user=current_user,
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


@community_blueprint.route("/community/<string:name>/join", methods=["POST"])
@login_required
def join_community(name):
    community = Community.query.filter_by(name=name).first_or_404()
    community_member = CommunityMember.query.filter_by(
        community_id=community.id, user_id=current_user.id
    ).first()
    if community_member == None:
        community_member = CommunityMember(community=community, app_user=current_user)
        db.session.add(community_member)
        db.session.commit()
    flash("Successfully joined community.", "primary")
    return redirect(url_for("community.community", name=community.name))


@community_blueprint.route("/community/<string:name>/leave", methods=["POST"])
@login_required
def leave_community(name):
    community = Community.query.filter_by(name=name).first_or_404()
    community_member = CommunityMember.query.filter_by(
        community_id=community.id, user_id=current_user.id
    ).first()
    if community_member != None:
        db.session.delete(community_member)
        db.session.commit()
    flash("Successfully left community.", "primary")
    return redirect(url_for("community.community", name=community.name))
