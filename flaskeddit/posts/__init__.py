from flask import Blueprint

posts_bp = Blueprint('posts_bp', __name__)

from flaskeddit.posts import routes
