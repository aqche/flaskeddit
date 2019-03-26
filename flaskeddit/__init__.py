from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from flaskeddit.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from flaskeddit.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from flaskeddit.post import post_blueprint
    app.register_blueprint(post_blueprint)

    from flaskeddit.posts import posts_blueprint
    app.register_blueprint(posts_blueprint)

    from flaskeddit.cli import cli_app_group
    app.cli.add_command(cli_app_group)

    return app
