from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from flaskeddit import db
from flaskeddit.community import community_blueprint
from flaskeddit.community.forms import CommunityForm
from flaskeddit.models import Community


@community_blueprint.route("/community/<string:name>")
def community(name):
    return "Recent {0} Community Posts".format(name)


@community_blueprint.route("/community/<int:community_id>/top")
def top_community_posts(community_id):
    return "Top Community Posts"


@community_blueprint.route("/community/create", methods=["GET", "POST"])
@login_required
def create_community():
    form = CommunityForm()
    if form.validate_on_submit():
        community = Community(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id,
        )
        db.session.add(community)
        db.session.commit()
        flash("Successfully created community.", "primary")
        return redirect(url_for("community.community", name=form.name.data))
    return render_template("create_community.jinja2", form=form)


@community_blueprint.route("/community/<int:community_id>/update")
@login_required
def update_community(community_id):
    return "Update Community"


@community_blueprint.route("/community/<int:community_id>/delete")
@login_required
def delete_community(community_id):
    return "Delete Community"
