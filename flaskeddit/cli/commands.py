from flaskeddit import db
from flaskeddit.cli import cli_app_group


@cli_app_group.command('create_db')
def create_db():
    db.create_all()
