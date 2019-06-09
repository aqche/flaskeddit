from flaskeddit import bcrypt, db
from flaskeddit.models import Community, Post, PostVote, User


class TestPost:
    def test_get_post(self, test_client):
        user = User(username="mockusername", password="mockpassword")
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

        response = test_client.get(f"/community/{community.name}/post/{post.title}")

        assert response is not None
        assert response.status_code == 200
        assert b"mockposttitle" in response.data

    def test_get_top_post(self, test_client):
        user = User(username="mockusername", password="mockpassword")
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

        response = test_client.get(f"/community/{community.name}/post/{post.title}")

        assert response is not None
        assert response.status_code == 200
        assert b"mockposttitle" in response.data

    def test_get_create_post(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        user = User(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", user=user
        )
        db.session.add(user)
        db.session.add(community)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.get(f"/community/{community.name}/post/create")

        assert response is not None
        assert response.status_code == 200
        assert b"Create Post" in response.data

    def test_post_create_post(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        user = User(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", user=user
        )
        db.session.add(user)
        db.session.add(community)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.post(
            f"/community/{community.name}/post/create",
            data={"title": "mockposttitle", "post": "mockpost"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully created post" in response.data

    def test_get_update_post(self, test_client):
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
            f"/community/{community.name}/post/{post.title}/update"
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Update Post" in response.data

    def test_post_update_post(self, test_client):
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
            f"/community/{community.name}/post/{post.title}/update",
            data={"post": "mockupdatedpost"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully updated post" in response.data

    def test_post_delete_post(self, test_client):
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
            f"/community/{community.name}/post/{post.title}/delete",
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully deleted post" in response.data

    def test_post_upvote_post(self, test_client):
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
            f"/community/{community.name}/post/{post.title}/upvote"
        )

        assert response is not None
        assert response.status_code == 302
        post_vote = PostVote.query.filter_by(user_id=user.id, post_id=post.id).first()
        assert post_vote is not None
        assert post_vote.vote == 1

    def test_post_downvote_post(self, test_client):
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
            f"/community/{community.name}/post/{post.title}/downvote"
        )

        assert response is not None
        assert response.status_code == 302
        post_vote = PostVote.query.filter_by(user_id=user.id, post_id=post.id).first()
        assert post_vote is not None
        assert post_vote.vote == -1
