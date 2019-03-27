from flaskeddit.communities import communities_blueprint


@communities_blueprint.route("/communities")
def communities():
    return "Recently Updated Communities"


@communities_blueprint.route("/communities/top")
def top_communities():
    return "Top Subscribed Communities"
