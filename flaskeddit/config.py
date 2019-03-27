import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(16))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
