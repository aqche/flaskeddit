from flaskeddit.cli import cli_app_group
from flaskeddit import db


@cli_app_group.command('create_db')
def create_db():
    db.create_all()
