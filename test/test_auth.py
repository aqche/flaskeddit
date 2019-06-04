class TestAuth:
    def test_register(self, test_client):
        response = test_client.get("/register")

        assert response is not None
        assert response.status_code == 200
        assert b"Register" in response.data
