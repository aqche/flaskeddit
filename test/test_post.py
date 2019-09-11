from test import helpers

from flaskeddit import bcrypt, db
from flaskeddit.models import AppUser, Community, Post, PostVote


class TestPost:
    def test_get_post(self, test_client):
        """Test GET request to the post route."""
        app_user = AppUser(username="mockusername", password="mockpassword")
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        post = Post(
            title="mockposttitle",
            post="mockpost",
            app_user=app_user,
            community=community,
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.add(post)
        db.session.commit()

        response = test_client.get(f"/community/{community.name}/post/{post.title}")

        assert response is not None
        assert response.status_code == 200
        assert bytes(post.title, "utf-8") in response.data

    def test_get_top_post(self, test_client):
        """Test GET request to the top post route."""
        app_user = AppUser(username="mockusername", password="mockpassword")
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        post = Post(
            title="mockposttitle",
            post="mockpost",
            app_user=app_user,
            community=community,
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.add(post)
        db.session.commit()

        response = test_client.get(f"/community/{community.name}/post/{post.title}")

        assert response is not None
        assert response.status_code == 200
        assert bytes(post.title, "utf-8") in response.data

    def test_get_create_post(self, test_client):
        """Test GET request to the create post route."""
        password = "Mockpassword123!"
        hashed_password = bcrypt.generate_password_hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.get(f"/community/{community.name}/post/create")

        assert response is not None
        assert response.status_code == 200
        assert b"Create Post" in response.data

    def test_post_create_post(self, test_client):
        """Test POST request to the create post route."""
        password = "Mockpassword123!"
        hashed_password = bcrypt.generate_password_hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.post(
            f"/community/{community.name}/post/create",
            data={"title": "mockposttitle", "post": "mockpost"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully created post" in response.data

    def test_get_update_post(self, test_client):
        """Test GET request to the update post route."""
        password = "Mockpassword123!"
        hashed_password = bcrypt.generate_password_hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        post = Post(
            title="mockposttitle",
            post="mockpost",
            app_user=app_user,
            community=community,
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.add(post)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.get(
            f"/community/{community.name}/post/{post.title}/update"
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Update Post" in response.data

    def test_post_update_post(self, test_client):
        """Test POST request to the update post route."""
        password = "Mockpassword123!"
        hashed_password = bcrypt.generate_password_hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        post = Post(
            title="mockposttitle",
            post="mockpost",
            app_user=app_user,
            community=community,
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.add(post)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.post(
            f"/community/{community.name}/post/{post.title}/update",
            data={"post": "mockupdatedpost"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully updated post" in response.data

    def test_post_delete_post(self, test_client):
        """Test POST request to the delete post route."""
        password = "Mockpassword123!"
        hashed_password = bcrypt.generate_password_hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        post = Post(
            title="mockposttitle",
            post="mockpost",
            app_user=app_user,
            community=community,
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.add(post)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.post(
            f"/community/{community.name}/post/{post.title}/delete",
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully deleted post" in response.data

    def test_post_upvote_post(self, test_client):
        """Test POST request to the upvote post route."""
        password = "Mockpassword123!"
        hashed_password = bcrypt.generate_password_hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        post = Post(
            title="mockposttitle",
            post="mockpost",
            app_user=app_user,
            community=community,
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.add(post)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.post(
            f"/community/{community.name}/post/{post.title}/upvote"
        )

        assert response is not None
        assert response.status_code == 302
        post_vote = PostVote.query.filter_by(
            user_id=app_user.id, post_id=post.id
        ).first()
        assert post_vote is not None
        assert post_vote.vote == 1

    def test_post_downvote_post(self, test_client):
        """Test POST request to the downvote post route."""
        password = "Mockpassword123!"
        hashed_password = bcrypt.generate_password_hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        post = Post(
            title="mockposttitle",
            post="mockpost",
            app_user=app_user,
            community=community,
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.add(post)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.post(
            f"/community/{community.name}/post/{post.title}/downvote"
        )

        assert response is not None
        assert response.status_code == 302
        post_vote = PostVote.query.filter_by(
            user_id=app_user.id, post_id=post.id
        ).first()
        assert post_vote is not None
        assert post_vote.vote == -1
