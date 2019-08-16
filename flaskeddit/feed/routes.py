from flask import render_template, request
from flask_login import current_user

from flaskeddit import db
from flaskeddit.feed import feed_blueprint
from flaskeddit.models import AppUser, Community, CommunityMember, Post, PostVote


@feed_blueprint.route("/")
@feed_blueprint.route("/feed")
def feed():
    """Route for list of posts from joined communities sorted by date created."""
    page = int(request.args.get("page", 1))
    if current_user.is_authenticated:
        posts = (
            db.session.query(
                Post.title,
                Post.post,
                Post.date_created,
                db.func.coalesce(db.func.sum(PostVote.vote), 0).label("votes"),
                AppUser.username,
                Community.name.label("community_name"),
            )
            .outerjoin(PostVote, Post.id == PostVote.post_id)
            .join(AppUser, Post.user_id == AppUser.id)
            .join(Community, Post.community_id == Community.id)
            .join(CommunityMember, Post.community_id == CommunityMember.community_id)
            .filter(CommunityMember.user_id == current_user.id)
            .group_by(Post.id, AppUser.id, Community.id)
            .order_by(Post.date_created.desc())
            .paginate(page=page, per_page=5)
        )
        return render_template("feed.jinja2", page="recent", posts=posts)
    else:
        return render_template("feed.jinja2", page="recent", posts=None)


@feed_blueprint.route("/feed/top")
def top_feed():
    """Route for list of posts from joined communities sorted by upvotes."""
    page = int(request.args.get("page", 1))
    if current_user.is_authenticated:
        posts = (
            db.session.query(
                Post.title,
                Post.post,
                Post.date_created,
                db.func.coalesce(db.func.sum(PostVote.vote), 0).label("votes"),
                AppUser.username,
                Community.name.label("community_name"),
            )
            .outerjoin(PostVote, Post.id == PostVote.post_id)
            .join(AppUser, Post.user_id == AppUser.id)
            .join(Community, Post.community_id == Community.id)
            .join(CommunityMember, Post.community_id == CommunityMember.community_id)
            .filter(CommunityMember.user_id == current_user.id)
            .group_by(Post.id, AppUser.id, Community.id)
            .order_by(db.literal_column("votes").desc())
            .paginate(page=page, per_page=5)
        )
        return render_template("feed.jinja2", page="top", posts=posts)
    else:
        return render_template("feed.jinja2", page="top", posts=None)
