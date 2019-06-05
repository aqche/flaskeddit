import pytest

from flaskeddit import create_app, db


@pytest.fixture()
def test_client():
    app = create_app()
    app.app_context().push()
    app.config["WTF_CSRF_ENABLED"] = False
    db.create_all()
    yield app.test_client()
    db.drop_all()
