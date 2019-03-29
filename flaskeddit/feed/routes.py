from flask import render_template
from flask_login import current_user

from flaskeddit.feed import feed_blueprint


@feed_blueprint.route("/")
@feed_blueprint.route("/feed")
def feed():
    if current_user.is_authenticated:
        return render_template("feed.jinja2")
    else:
        return render_template("feed.jinja2")


@feed_blueprint.route("/feed/top")
def top_feed():
    if current_user.is_authenticated:
        return "Top Posts"
    else:
        return "Subscribed Communities' Top Posts"
