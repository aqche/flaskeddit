from flaskeddit import db
from flaskeddit.models import Community, User


class TestCommunities:
    def test_get_communities(self, test_client):
        user = User(username="mockusername", password="mockpassword")
        commuity = Community(
            name="mockcommunity", description="mockdescription", user=user
        )
        db.session.add(user)
        db.session.add(commuity)
        db.session.commit()

        response = test_client.get("/communities")

        assert response is not None
        assert response.status_code == 200
        assert b"mockcommunity" in response.data

    def test_get_top_communities(self, test_client):
        user = User(username="mockusername", password="mockpassword")
        commuity = Community(
            name="mockcommunity", description="mockdescription", user=user
        )
        db.session.add(user)
        db.session.add(commuity)
        db.session.commit()

        response = test_client.get("/communities/top")

        assert response is not None
        assert response.status_code == 200
        assert b"mockcommunity" in response.data
