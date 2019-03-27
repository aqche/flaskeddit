from flask_login import login_required

from flaskeddit.community import community_blueprint


@community_blueprint.route("/community/<int:community_id>")
def community(community_id):
    return "Recent Community Posts"


@community_blueprint.route("/community/<int:community_id>/top")
def top_community_posts(community_id):
    return "Top Community Posts"


@community_blueprint.route("/community/create")
@login_required
def create_community():
    return "Create Community"


@community_blueprint.route("/community/<int:community_id>/update")
@login_required
def update_community(community_id):
    return "Update Community"


@community_blueprint.route("/community/<int:community_id>/delete")
@login_required
def delete_community(community_id):
    return "Delete Community"
