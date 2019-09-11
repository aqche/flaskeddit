from flaskeddit import db
from flaskeddit.models import AppUser, Community, CommunityMember, Post, PostVote


def get_community(name):
    """Gets a community."""
    community = Community.query.filter_by(name=name).first()
    return community


def create_community(name, description, app_user):
    """Creates a new community."""
    community = Community(name=name, description=description, app_user=app_user)
    db.session.add(community)
    db.session.commit()


def update_community(community, description):
    """Updates a community description."""
    community.description = description
    db.session.commit()


def delete_community(community):
    """Deletes a community."""
    db.session.delete(community)
    db.session.commit()


def get_posts(community_id, page, ordered_by_votes):
    """Gets posts from a community by date created."""
    ordered_by = Post.date_created.desc()
    if ordered_by_votes:
        ordered_by = db.literal_column("votes").desc()
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
        .filter(Post.community_id == community_id)
        .group_by(Post.id, AppUser.id)
        .order_by(ordered_by)
        .paginate(page=page, per_page=5)
    )
    return posts


def get_community_member(community_id, user_id):
    """Gets a community member."""
    community_member = CommunityMember.query.filter_by(
        community_id=community_id, user_id=user_id
    ).first()
    return community_member


def create_community_member(community, app_user):
    """Creates a community member."""
    community_member = CommunityMember(community=community, app_user=app_user)
    db.session.add(community_member)
    db.session.commit()


def delete_community_member(community_member):
    """Deletes a community member."""
    db.session.delete(community_member)
    db.session.commit()
