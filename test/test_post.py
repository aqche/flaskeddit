from test import helpers

from flaskeddit.auth import auth_service
from flaskeddit.community import community_service
from flaskeddit.models import PostVote
from flaskeddit.post import post_service
from flaskeddit.user import user_service


class TestPost:
    def test_get_post(self, test_client):
        """Test GET request to the post route."""
        username = "mockusername"
        community_name = "mockcommunity"
        post_title = "mockposttitle"
        auth_service.register_user(username, "Mockpassword123!")
        user = user_service.get_user(username)
        community_service.create_community(community_name, "mockdescription", user)
        post_service.create_post(
            post_title,
            "mockpost",
            community_service.get_community(community_name),
            user,
        )

        response = test_client.get(f"/community/{community_name}/post/{post_title}")

        assert response is not None
        assert response.status_code == 200
        assert bytes(post_title, "utf-8") in response.data

    def test_get_top_post(self, test_client):
        """Test GET request to the top post route."""
        username = "mockusername"
        community_name = "mockcommunity"
        post_title = "mockposttitle"
        auth_service.register_user(username, "Mockpassword123!")
        user = user_service.get_user(username)
        community_service.create_community(community_name, "mockdescription", user)
        post_service.create_post(
            post_title,
            "mockpost",
            community_service.get_community(community_name),
            user,
        )

        response = test_client.get(f"/community/{community_name}/post/{post_title}")

        assert response is not None
        assert response.status_code == 200
        assert bytes(post_title, "utf-8") in response.data

    def test_get_create_post(self, test_client):
        """Test GET request to the create post route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        auth_service.register_user(username, password)
        community_service.create_community(
            community_name, "mockdescription", user_service.get_user(username)
        )
        helpers.login(test_client, username, password)

        response = test_client.get(f"/community/{community_name}/post/create")

        assert response is not None
        assert response.status_code == 200
        assert b"Create Post" in response.data

    def test_post_create_post(self, test_client):
        """Test POST request to the create post route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        auth_service.register_user(username, password)
        community_service.create_community(
            community_name, "mockdescription", user_service.get_user(username)
        )
        helpers.login(test_client, username, password)

        response = test_client.post(
            f"/community/{community_name}/post/create",
            data={"title": "mockposttitle", "post": "mockpost"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully created post" in response.data

    def test_get_update_post(self, test_client):
        """Test GET request to the update post route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        post_title = "mockposttitle"
        auth_service.register_user(username, password)
        user = user_service.get_user(username)
        community_service.create_community(community_name, "mockdescription", user)
        post_service.create_post(
            post_title,
            "mockpost",
            community_service.get_community(community_name),
            user,
        )
        helpers.login(test_client, username, password)

        response = test_client.get(
            f"/community/{community_name}/post/{post_title}/update"
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Update Post" in response.data

    def test_post_update_post(self, test_client):
        """Test POST request to the update post route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        post_title = "mockposttitle"
        auth_service.register_user(username, password)
        user = user_service.get_user(username)
        community_service.create_community(community_name, "mockdescription", user)
        post_service.create_post(
            post_title,
            "mockpost",
            community_service.get_community(community_name),
            user,
        )
        helpers.login(test_client, username, password)

        response = test_client.post(
            f"/community/{community_name}/post/{post_title}/update",
            data={"post": "mockupdatedpost"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully updated post" in response.data

    def test_post_delete_post(self, test_client):
        """Test POST request to the delete post route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        post_title = "mockposttitle"
        auth_service.register_user(username, password)
        user = user_service.get_user(username)
        community_service.create_community(community_name, "mockdescription", user)
        post_service.create_post(
            post_title,
            "mockpost",
            community_service.get_community(community_name),
            user,
        )
        helpers.login(test_client, username, password)

        response = test_client.post(
            f"/community/{community_name}/post/{post_title}/delete",
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully deleted post" in response.data

    def test_post_upvote_post(self, test_client):
        """Test POST request to the upvote post route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        post_title = "mockposttitle"
        auth_service.register_user(username, password)
        user = user_service.get_user(username)
        community_service.create_community(community_name, "mockdescription", user)
        post_service.create_post(
            post_title,
            "mockpost",
            community_service.get_community(community_name),
            user,
        )
        helpers.login(test_client, username, password)

        response = test_client.post(
            f"/community/{community_name}/post/{post_title}/upvote"
        )

        assert response is not None
        assert response.status_code == 302
        post_vote = PostVote.query.filter_by(
            user_id=user.id,
            post_id=post_service.get_post(post_title, community_name).id,
        ).first()
        assert post_vote is not None
        assert post_vote.vote == 1

    def test_post_downvote_post(self, test_client):
        """Test POST request to the downvote post route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        post_title = "mockposttitle"
        auth_service.register_user(username, password)
        user = user_service.get_user(username)
        community_service.create_community(community_name, "mockdescription", user)
        post_service.create_post(
            post_title,
            "mockpost",
            community_service.get_community(community_name),
            user,
        )
        helpers.login(test_client, username, password)

        response = test_client.post(
            f"/community/{community_name}/post/{post_title}/downvote"
        )

        assert response is not None
        assert response.status_code == 302
        post_vote = PostVote.query.filter_by(
            user_id=user.id,
            post_id=post_service.get_post(post_title, community_name).id,
        ).first()
        assert post_vote is not None
        assert post_vote.vote == -1
