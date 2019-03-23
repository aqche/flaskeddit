from flask import Flask
from flaskeddit.config import Config


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    from flaskeddit.auth import auth_bp
    from flaskeddit.post import post_bp
    from flaskeddit.posts import posts_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(posts_bp)

    return app
