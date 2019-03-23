from flask import Blueprint

posts_blueprint = Blueprint('posts', __name__)

from flaskeddit.posts import routes
