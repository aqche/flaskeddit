from flaskeddit import db
from flaskeddit.models import AppUser


class TestUser:
    def test_get_user(self, test_client):
        app_user = AppUser(username="mockusername", password="mockpassword")
        db.session.add(app_user)
        db.session.commit()

        response = test_client.get(f"/user/{app_user.username}")

        assert response is not None
        assert response.status_code == 200
        assert b"mockusername" in response.data
