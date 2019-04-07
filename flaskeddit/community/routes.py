from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from flaskeddit import db
from flaskeddit.community import community_blueprint
from flaskeddit.community.forms import CommunityForm, UpdateCommunityForm
from flaskeddit.models import Community


@community_blueprint.route("/community/<string:name>")
def community(name):
    page = int(request.args.get("page", 1))
    community = Community.query.filter_by(name=name).first_or_404()
    posts = community.posts.paginate(page=page, per_page=5)
    return render_template(
        "community.jinja2", page="recent", community=community, posts=posts
    )


@community_blueprint.route("/community/<string:name>/top")
def top_community(name):
    # TODO: Update to sort by most replied/votes?
    page = int(request.args.get("page", 1))
    community = Community.query.filter_by(name=name).first_or_404()
    posts = community.posts.paginate(page=page, per_page=5)
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
        return redirect(url_for("community.community", name=form.name.data))
    return render_template("create_community.jinja2", form=form)


@community_blueprint.route("/community/<string:name>/update", methods=["GET", "POST"])
@login_required
def update_community(name):
    community = Community.query.filter_by(name=name).first_or_404()
    if current_user.id != community.user_id:
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
    if current_user.id != community.user_id:
        return redirect(url_for("community.community", name=name))
    db.session.delete(community)
    db.session.commit()
    flash("Successfully deleted community.", "primary")
    return redirect(url_for("feed.feed"))
