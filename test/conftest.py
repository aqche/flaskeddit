import pytest

from flaskeddit import create_app, db


@pytest.fixture(scope="class")
def test_client():
    app = create_app()
    with app.app_context():
        db.create_all()
    yield app.test_client()
    with app.app_context():
        db.drop_all()
