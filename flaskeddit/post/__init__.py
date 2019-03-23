from flask import Blueprint

post_bp = Blueprint('post_bp', __name__)

from flaskeddit.post import routes
