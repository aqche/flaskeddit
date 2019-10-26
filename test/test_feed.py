from test import helpers

from passlib.hash import bcrypt

from flaskeddit import db
from flaskeddit.models import AppUser, Community, CommunityMember, Post


class TestFeed:
    def test_get_feed(self, test_client):
        """
        Test GET request to the / route to assert posts from the users joined
        communities are displayed.
        """
        password = "Mockpassword123!"
        hashed_password = bcrypt.hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        community_member = CommunityMember(app_user=app_user, community=community)
        post = Post(
            title="mockposttitle",
            post="mockpost",
            app_user=app_user,
            community=community,
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.add(community_member)
        db.session.add(post)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.get("/")

        assert response is not None
        assert response.status_code == 200
        assert bytes(post.title, "utf-8") in response.data

    def test_get_top_feed(self, test_client):
        """
        Test GET request to the /feed/top route to assert posts from the users joined
        communities are displayed.
        """
        password = "Mockpassword123!"
        hashed_password = bcrypt.hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        community_member = CommunityMember(app_user=app_user, community=community)
        post = Post(
            title="mockposttitle",
            post="mockpost",
            app_user=app_user,
            community=community,
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.add(community_member)
        db.session.add(post)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.get("/feed/top")

        assert response is not None
        assert response.status_code == 200
        assert bytes(post.title, "utf-8") in response.data
