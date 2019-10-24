from test import helpers

from flaskeddit import bcrypt, db
from flaskeddit.models import AppUser


class TestAuth:
    def test_get_register(self, test_client):
        """
        Tests GET request to the /register route to assert the registration page is
        returned.
        """
        response = test_client.get("/register")

        assert response is not None
        assert response.status_code == 200
        assert b"Register" in response.data

    def test_post_register(self, test_client):
        """
        Test POST request to the /register route to assert the user is successfully
        registered.
        """
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
        """
        Test GET request to the /login route to assert the login page is returned.
        """
        response = test_client.get("/login")

        assert response is not None
        assert response.status_code == 200
        assert b"Log In" in response.data

    def test_post_login(self, test_client):
        """
        Test POST request to the /login route to assert the user is successfully logged
        in.
        """
        password = "Mockpassword123!"
        hashed_password = bcrypt.generate_password_hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        db.session.add(app_user)
        db.session.commit()

        response = test_client.post(
            "/login",
            data={"username": app_user.username, "password": password},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully logged in" in response.data

    def test_post_logout(self, test_client):
        """
        Test POST request to the /logout route to assert the user is successfully
        logged out.
        """
        password = "Mockpassword123!"
        hashed_password = bcrypt.generate_password_hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        db.session.add(app_user)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.post("/logout", follow_redirects=True)

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully logged out" in response.data
