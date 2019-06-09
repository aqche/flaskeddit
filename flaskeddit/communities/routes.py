from flask import render_template, request

from flaskeddit import db
from flaskeddit.communities import communities_blueprint
from flaskeddit.models import AppUser, Community, CommunityMember


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
            AppUser.username,
        )
        .join(AppUser, Community.user_id == AppUser.id)
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
            AppUser.username,
            db.func.count(CommunityMember.id).label("community_members"),
        )
        .join(AppUser, Community.user_id == AppUser.id)
        .outerjoin(CommunityMember, Community.id == CommunityMember.community_id)
        .group_by(Community.id)
        .order_by(db.literal_column("community_members").desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("communities.jinja2", page="top", communities=communities)
