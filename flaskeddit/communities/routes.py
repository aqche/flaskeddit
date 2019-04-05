from flask import render_template

from flaskeddit import db
from flaskeddit.communities import communities_blueprint
from flaskeddit.models import Community, User


@communities_blueprint.route("/communities")
def communities():
    communities = (
        db.session.query(Community, User.username)
        .join(Community, Community.user_id == User.id)
        .order_by(Community.date_created.desc())
        .all()
    )
    return render_template("communities.jinja2", page="recent", communities=communities)


@communities_blueprint.route("/communities/top")
def top_communities():
    # TODO: Update to sort by most joined
    communities = (
        db.session.query(Community, User.username)
        .join(Community, Community.user_id == User.id)
        .order_by(Community.date_created.desc())
        .all()
    )
    return render_template("communities.jinja2", page="top", communities=communities)
