from flaskeddit import db
from flaskeddit.models import User


class TestUser:
    def test_get_user(self, test_client):
        user = User(username="mockusername", password="mockpassword")
        db.session.add(user)
        db.session.commit()

        response = test_client.get(f"/user/{user.username}")

        assert response is not None
        assert response.status_code == 200
        assert b"mockusername" in response.data
