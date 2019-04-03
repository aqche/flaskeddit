from flask import render_template

from flaskeddit.communities import communities_blueprint
from flaskeddit.models import Community


@communities_blueprint.route("/communities")
def communities():
    communities = Community.query.order_by(Community.date_created.desc()).all()
    return render_template("communities.jinja2", communities=communities)


@communities_blueprint.route("/communities/top")
def top_communities():
    return "Top Subscribed Communities"
