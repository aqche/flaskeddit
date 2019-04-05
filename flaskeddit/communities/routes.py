from flask import render_template, request

from flaskeddit import db
from flaskeddit.communities import communities_blueprint
from flaskeddit.models import Community, User


@communities_blueprint.route("/communities")
def communities():
    page = int(request.args.get("page", 1))
    communities = (
        db.session.query(Community, User.username)
        .join(Community, Community.user_id == User.id)
        .order_by(Community.date_created.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("communities.jinja2", page="recent", communities=communities)


@communities_blueprint.route("/communities/top")
def top_communities():
    # TODO: Update to sort by most joined
    page = int(request.args.get("page", 1))
    communities = (
        db.session.query(Community, User.username)
        .join(Community, Community.user_id == User.id)
        .order_by(Community.date_created.desc())
        .paginate(page=page, per_page=1)
    )
    return render_template("communities.jinja2", page="top", communities=communities)
