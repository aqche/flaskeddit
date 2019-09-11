from test import helpers

from flaskeddit.auth import auth_service
from flaskeddit.community import community_service
from flaskeddit.user import user_service


class TestCommunity:
    def test_get_community(self, test_client):
        """Test GET request to the community route."""
        username = "mockusername"
        community_name = "mockcommunity"
        auth_service.register_user(username, "Mockpassword123!")
        community_service.create_community(
            community_name, "mockdescription", user_service.get_user(username)
        )

        response = test_client.get(f"/community/{community_name}")

        assert response is not None
        assert response.status_code == 200
        assert bytes(community_name, "utf-8") in response.data

    def test_get_top_community(self, test_client):
        """Test GET request to the top community route."""
        username = "mockusername"
        community_name = "mockcommunity"
        auth_service.register_user(username, "Mockpassword123!")
        community_service.create_community(
            community_name, "mockdescription", user_service.get_user(username)
        )

        response = test_client.get(f"/community/{community_name}/top")

        assert response is not None
        assert response.status_code == 200
        assert bytes(community_name, "utf-8") in response.data

    def test_get_create_community(self, test_client):
        """Test GET request to the create community route."""
        username = "mockusername"
        password = "Mockpassword123!"
        auth_service.register_user(username, password)
        helpers.login(test_client, username, password)

        response = test_client.get("/community/create")

        assert response is not None
        assert response.status_code == 200
        assert b"Create Community" in response.data

    def test_post_create_community(self, test_client):
        """Test POST request to the create community route."""
        username = "mockusername"
        password = "Mockpassword123!"
        auth_service.register_user(username, password)
        helpers.login(test_client, username, password)

        response = test_client.post(
            "/community/create",
            data={"name": "mockcommunity", "description": "mockdescription"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully created community" in response.data

    def test_get_update_community(self, test_client):
        """Test GET request to the update community route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        auth_service.register_user(username, password)
        community_service.create_community(
            community_name, "mockdescription", user_service.get_user(username)
        )
        helpers.login(test_client, username, password)

        response = test_client.get(f"/community/{community_name}/update")

        assert response is not None
        assert response.status_code == 200
        assert b"Update Community" in response.data

    def test_post_update_community(self, test_client):
        """Test POST request to the update community route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        auth_service.register_user(username, password)
        community_service.create_community(
            community_name, "mockdescription", user_service.get_user(username)
        )
        helpers.login(test_client, username, password)

        response = test_client.post(
            f"/community/{community_name}/update",
            data={"description": "mockupdateddescription"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully updated community" in response.data

    def test_post_delete_community(self, test_client):
        """Test POST request to the delete community route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        auth_service.register_user(username, password)
        community_service.create_community(
            community_name, "mockdescription", user_service.get_user(username)
        )
        helpers.login(test_client, username, password)

        response = test_client.post(
            f"/community/{community_name}/delete", follow_redirects=True
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully deleted community" in response.data

    def test_post_join_community(self, test_client):
        """Test POST request to the join community route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        auth_service.register_user(username, password)
        community_service.create_community(
            community_name, "mockdescription", user_service.get_user(username)
        )
        helpers.login(test_client, username, password)

        response = test_client.post(
            f"/community/{community_name}/join", follow_redirects=True
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully joined community" in response.data

    def test_post_leave_community(self, test_client):
        """Test POST request to the leave community route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        auth_service.register_user(username, password)
        community_service.create_community(
            community_name, "mockdescription", user_service.get_user(username)
        )
        helpers.login(test_client, username, password)

        response = test_client.post(
            f"/community/{community_name}/leave", follow_redirects=True
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully left community" in response.data
