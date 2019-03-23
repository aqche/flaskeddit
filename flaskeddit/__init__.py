from flask import Flask


def create_app():
    app = Flask(__name__)

    from flaskeddit.auth import auth_bp
    from flaskeddit.post import post_bp
    from flaskeddit.posts import posts_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(posts_bp)

    return app
