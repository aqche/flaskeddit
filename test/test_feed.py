from test import helpers

from flaskeddit.auth import auth_service
from flaskeddit.community import community_service
from flaskeddit.post import post_service
from flaskeddit.user import user_service


class TestFeed:
    def test_get_feed(self, test_client):
        """Test GET request to the feed route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        post_title = "mockposttitle"
        auth_service.register_user(username, password)
        user = user_service.get_user(username)
        community_service.create_community(community_name, "mockdescription", user)
        community = community_service.get_community(community_name)
        community_service.create_community_member(community, user)
        post_service.create_post(post_title, "mockpost", community, user)
        helpers.login(test_client, username, password)

        response = test_client.get("/")

        assert response is not None
        assert response.status_code == 200
        assert bytes(post_title, "utf-8") in response.data

    def test_get_top_feed(self, test_client):
        """Test GET request to the top feed route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        post_title = "mockposttitle"
        auth_service.register_user(username, password)
        user = user_service.get_user(username)
        community_service.create_community(community_name, "mockdescription", user)
        community = community_service.get_community(community_name)
        community_service.create_community_member(community, user)
        post_service.create_post(post_title, "mockpost", community, user)
        helpers.login(test_client, username, password)

        response = test_client.get("/feed/top")

        assert response is not None
        assert response.status_code == 200
        assert bytes(post_title, "utf-8") in response.data
