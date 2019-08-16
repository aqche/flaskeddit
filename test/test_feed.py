from flaskeddit import bcrypt, db
from flaskeddit.models import AppUser, Community, CommunityMember, Post


class TestFeed:
    def test_get_feed(self, test_client):
        """Test GET request to the feed route."""
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
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
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.get("/")

        assert response is not None
        assert response.status_code == 200
        assert b"mockposttitle" in response.data

    def test_get_top_feed(self, test_client):
        """Test GET request to the top feed route."""
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
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
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.get("/feed/top")

        assert response is not None
        assert response.status_code == 200
        assert b"mockposttitle" in response.data
