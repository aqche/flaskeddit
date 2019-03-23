import os


class Config():
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(16))
