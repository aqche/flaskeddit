from test import helpers

from flaskeddit.auth import auth_service


class TestAuth:
    def test_get_register(self, test_client):
        """Test GET request to the register route."""
        response = test_client.get("/register")

        assert response is not None
        assert response.status_code == 200
        assert b"Register" in response.data

    def test_post_register(self, test_client):
        """Test POST request to the register route."""
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
        """Test GET request to the login route."""
        response = test_client.get("/login")

        assert response is not None
        assert response.status_code == 200
        assert b"Log In" in response.data

    def test_post_login(self, test_client):
        """Test POST request to the login route."""
        username = "mockusername"
        password = "Mockpassword123!"
        auth_service.register_user(username, password)

        response = test_client.post(
            "/login",
            data={"username": username, "password": password},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully logged in" in response.data

    def test_post_logout(self, test_client):
        """Test POST request to the logout route."""
        username = "mockusername"
        password = "Mockpassword123!"
        auth_service.register_user(username, password)
        helpers.login(test_client, username, password)

        response = test_client.post("/logout", follow_redirects=True)

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully logged out" in response.data
