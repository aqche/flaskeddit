from flaskeddit.auth import auth_service
from flaskeddit.community import community_service
from flaskeddit.user import user_service


class TestCommunities:
    def test_get_communities(self, test_client):
        """Test GET request to the communities route."""
        username = "mockusername"
        community_name = "mockcommunity"
        auth_service.register_user(username, "Mockpassword123!")
        community_service.create_community(
            community_name, "mockdescription", user_service.get_user(username)
        )

        response = test_client.get("/communities")

        assert response is not None
        assert response.status_code == 200
        assert bytes(community_name, "utf-8") in response.data

    def test_get_top_communities(self, test_client):
        """Test GET request to the top communities route."""
        username = "mockusername"
        community_name = "mockcommunity"
        auth_service.register_user(username, "Mockpassword123!")
        community_service.create_community(
            community_name, "mockdescription", user_service.get_user(username)
        )

        response = test_client.get("/communities/top")

        assert response is not None
        assert response.status_code == 200
        assert bytes(community_name, "utf-8") in response.data
