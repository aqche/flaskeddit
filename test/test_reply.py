from flaskeddit import bcrypt, db
from flaskeddit.models import Community, Post, Reply, ReplyVote, User


class TestReply:
    def test_get_reply(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        user = User(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", user=user
        )
        post = Post(
            title="mockposttitle", post="mockpost", user=user, community=community
        )
        db.session.add(user)
        db.session.add(community)
        db.session.add(post)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.get(
            f"/community/{community.name}/post/{post.title}/reply"
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Create Reply" in response.data

    def test_post_reply(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        user = User(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", user=user
        )
        post = Post(
            title="mockposttitle", post="mockpost", user=user, community=community
        )
        db.session.add(user)
        db.session.add(community)
        db.session.add(post)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.post(
            f"/community/{community.name}/post/{post.title}/reply",
            data={"reply": "mockreply"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully created reply" in response.data

    def test_get_update_reply(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        user = User(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", user=user
        )
        post = Post(
            title="mockposttitle", post="mockpost", user=user, community=community
        )
        reply = Reply(reply="mockreply", user=user, post=post)
        db.session.add(user)
        db.session.add(community)
        db.session.add(post)
        db.session.add(reply)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.get(
            f"/community/{community.name}/post/{post.title}/reply/{reply.id}/edit"
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Update Reply" in response.data

    def test_post_update_reply(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        user = User(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", user=user
        )
        post = Post(
            title="mockposttitle", post="mockpost", user=user, community=community
        )
        reply = Reply(reply="mockreply", user=user, post=post)
        db.session.add(user)
        db.session.add(community)
        db.session.add(post)
        db.session.add(reply)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.post(
            f"/community/{community.name}/post/{post.title}/reply/{reply.id}/edit",
            data={"reply": "mockupdatedreply"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully updated reply" in response.data

    def test_post_delete_reply(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        user = User(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", user=user
        )
        post = Post(
            title="mockposttitle", post="mockpost", user=user, community=community
        )
        reply = Reply(reply="mockreply", user=user, post=post)
        db.session.add(user)
        db.session.add(community)
        db.session.add(post)
        db.session.add(reply)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.post(
            f"/community/{community.name}/post/{post.title}/reply/{reply.id}/delete",
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully deleted reply" in response.data

    def test_post_upvote_reply(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        user = User(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", user=user
        )
        post = Post(
            title="mockposttitle", post="mockpost", user=user, community=community
        )
        reply = Reply(reply="mockreply", user=user, post=post)
        db.session.add(user)
        db.session.add(community)
        db.session.add(post)
        db.session.add(reply)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.post(
            f"/community/{community.name}/post/{post.title}/reply/{reply.id}/upvote"
        )

        assert response is not None
        assert response.status_code == 302
        reply_vote = ReplyVote.query.filter_by(
            user_id=user.id, reply_id=reply.id
        ).first()
        assert reply_vote is not None
        assert reply_vote.vote == 1

    def test_post_downvote_reply(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        user = User(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", user=user
        )
        post = Post(
            title="mockposttitle", post="mockpost", user=user, community=community
        )
        reply = Reply(reply="mockreply", user=user, post=post)
        db.session.add(user)
        db.session.add(community)
        db.session.add(post)
        db.session.add(reply)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.post(
            f"/community/{community.name}/post/{post.title}/reply/{reply.id}/downvote"
        )

        assert response is not None
        assert response.status_code == 302
        reply_vote = ReplyVote.query.filter_by(
            user_id=user.id, reply_id=reply.id
        ).first()
        assert reply_vote is not None
        assert reply_vote.vote == -1
