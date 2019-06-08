from flaskeddit import bcrypt, db
from flaskeddit.models import User


class TestAuth:
    def test_get_register(self, test_client):
        response = test_client.get("/register")

        assert response is not None
        assert response.status_code == 200
        assert b"Register" in response.data

    def test_post_register(self, test_client):
        response = test_client.post(
            "/register",
            data={
                "username": "mockusername",
                "password": "Mockpassword123!",
                "confirm_password": "Mockpassword123!",
            },
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully registered." in response.data

    def test_get_login(self, test_client):
        response = test_client.get("/login")

        assert response is not None
        assert response.status_code == 200
        assert b"Log In" in response.data

    def test_post_login(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        user = User(username="mockusername", password=hashed_password)
        db.session.add(user)
        db.session.commit()

        response = test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully logged in" in response.data

    def test_post_logout(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        user = User(username="mockusername", password=hashed_password)
        db.session.add(user)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.post("/logout", follow_redirects=True)

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully logged out" in response.data
