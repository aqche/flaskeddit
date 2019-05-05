from flask import render_template, request

from flaskeddit import db
from flaskeddit.communities import communities_blueprint
from flaskeddit.models import Community, CommunityMember, User


@communities_blueprint.route("/communities")
def communities():
    page = int(request.args.get("page", 1))
    communities = (
        db.session.query(
            Community.id,
            Community.name,
            Community.description,
            Community.date_created,
            Community.user_id,
            User.username,
        )
        .join(User, Community.user_id == User.id)
        .order_by(Community.date_created.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("communities.jinja2", page="recent", communities=communities)


@communities_blueprint.route("/communities/top")
def top_communities():
    page = int(request.args.get("page", 1))
    communities = (
        db.session.query(
            Community.id,
            Community.name,
            Community.description,
            Community.date_created,
            Community.user_id,
            User.username,
            db.func.count(CommunityMember.id).label("community_members"),
        )
        .join(User, Community.user_id == User.id)
        .outerjoin(CommunityMember, Community.id == CommunityMember.community_id)
        .group_by(Community.id)
        .order_by(db.literal_column("community_members").desc())
        .paginate(page=page, per_page=5)
    )
    print(communities.items)
    return render_template("communities.jinja2", page="top", communities=communities)
