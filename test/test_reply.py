from test import helpers

from flaskeddit.auth import auth_service
from flaskeddit.community import community_service
from flaskeddit.models import Reply, ReplyVote
from flaskeddit.post import post_service
from flaskeddit.reply import reply_service
from flaskeddit.user import user_service


class TestReply:
    def test_get_reply(self, test_client):
        """Test GET request to the reply route."""
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
            f"/community/{community_name}/post/{post_title}/reply"
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Create Reply" in response.data

    def test_post_reply(self, test_client):
        """Test POST request to the reply route."""
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
            f"/community/{community_name}/post/{post_title}/reply",
            data={"reply": "mockreply"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully created reply" in response.data

    def test_get_update_reply(self, test_client):
        """Test GET request to the update reply route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        post_title = "mockposttitle"
        reply = "mockreply"
        auth_service.register_user(username, password)
        user = user_service.get_user(username)
        community_service.create_community(community_name, "mockdescription", user)
        post_service.create_post(
            post_title,
            "mockpost",
            community_service.get_community(community_name),
            user,
        )
        reply_service.create_reply(
            reply, post_service.get_post(post_title, community_name), user
        )
        helpers.login(test_client, username, password)

        response = test_client.get(
            f"/community/{community_name}/post/{post_title}/reply/{Reply.query.filter_by(reply=reply).first().id}/edit"
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Update Reply" in response.data

    def test_post_update_reply(self, test_client):
        """Test POST request to the update reply route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        post_title = "mockposttitle"
        reply = "mockreply"
        auth_service.register_user(username, password)
        user = user_service.get_user(username)
        community_service.create_community(community_name, "mockdescription", user)
        post_service.create_post(
            post_title,
            "mockpost",
            community_service.get_community(community_name),
            user,
        )
        reply_service.create_reply(
            reply, post_service.get_post(post_title, community_name), user
        )
        helpers.login(test_client, username, password)

        response = test_client.post(
            f"/community/{community_name}/post/{post_title}/reply/{Reply.query.filter_by(reply=reply).first().id}/edit",
            data={"reply": "mockupdatedreply"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully updated reply" in response.data

    def test_post_delete_reply(self, test_client):
        """Test POST request to the delete reply route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        post_title = "mockposttitle"
        reply = "mockreply"
        auth_service.register_user(username, password)
        user = user_service.get_user(username)
        community_service.create_community(community_name, "mockdescription", user)
        post_service.create_post(
            post_title,
            "mockpost",
            community_service.get_community(community_name),
            user,
        )
        reply_service.create_reply(
            reply, post_service.get_post(post_title, community_name), user
        )
        helpers.login(test_client, username, password)

        response = test_client.post(
            f"/community/{community_name}/post/{post_title}/reply/{Reply.query.filter_by(reply=reply).first().id}/delete",
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully deleted reply" in response.data

    def test_post_upvote_reply(self, test_client):
        """Test POST request to the upvote reply route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        post_title = "mockposttitle"
        reply = "mockreply"
        auth_service.register_user(username, password)
        user = user_service.get_user(username)
        community_service.create_community(community_name, "mockdescription", user)
        post_service.create_post(
            post_title,
            "mockpost",
            community_service.get_community(community_name),
            user,
        )
        reply_service.create_reply(
            reply, post_service.get_post(post_title, community_name), user
        )
        reply = Reply.query.filter_by(reply=reply).first()
        helpers.login(test_client, username, password)

        response = test_client.post(
            f"/community/{community_name}/post/{post_title}/reply/{reply.id}/upvote"
        )

        assert response is not None
        assert response.status_code == 302
        reply_vote = ReplyVote.query.filter_by(
            user_id=user.id, reply_id=reply.id
        ).first()
        assert reply_vote is not None
        assert reply_vote.vote == 1

    def test_post_downvote_reply(self, test_client):
        """Test POST request to the downvote reply route."""
        username = "mockusername"
        password = "Mockpassword123!"
        community_name = "mockcommunity"
        post_title = "mockposttitle"
        reply = "mockreply"
        auth_service.register_user(username, password)
        user = user_service.get_user(username)
        community_service.create_community(community_name, "mockdescription", user)
        post_service.create_post(
            post_title,
            "mockpost",
            community_service.get_community(community_name),
            user,
        )
        reply_service.create_reply(
            reply, post_service.get_post(post_title, community_name), user
        )
        reply = Reply.query.filter_by(reply=reply).first()
        helpers.login(test_client, username, password)

        response = test_client.post(
            f"/community/{community_name}/post/{post_title}/reply/{reply.id}/downvote"
        )

        assert response is not None
        assert response.status_code == 302
        reply_vote = ReplyVote.query.filter_by(
            user_id=user.id, reply_id=reply.id
        ).first()
        assert reply_vote is not None
        assert reply_vote.vote == -1
