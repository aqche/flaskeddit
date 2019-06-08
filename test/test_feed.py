from flaskeddit import bcrypt, db
from flaskeddit.models import Community, CommunityMember, Post, User


class TestFeed:
    def test_get_feed(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        user = User(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", user=user
        )
        community_member = CommunityMember(user=user, community=community)
        post = Post(
            title="mockposttitle", post="mockpost", user=user, community=community
        )
        db.session.add(user)
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
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        user = User(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", user=user
        )
        community_member = CommunityMember(user=user, community=community)
        post = Post(
            title="mockposttitle", post="mockpost", user=user, community=community
        )
        db.session.add(user)
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
