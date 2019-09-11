from flaskeddit.auth import auth_service


class TestUser:
    def test_get_user(self, test_client):
        username = "mockusername"
        auth_service.register_user(username, "Mockpassword123!")

        response = test_client.get(f"/user/{username}")

        assert response is not None
        assert response.status_code == 200
        assert bytes(username, "utf-8") in response.data
