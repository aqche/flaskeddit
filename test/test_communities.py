from flaskeddit import db
from flaskeddit.models import AppUser, Community


class TestCommunities:
    def test_get_communities(self, test_client):
        """
        Test GET request to the /communities route to assert the page displays existing
        communities.
        """
        app_user = AppUser(username="mockusername", password="mockpassword")
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()

        response = test_client.get("/communities")

        assert response is not None
        assert response.status_code == 200
        assert bytes(community.name, "utf-8") in response.data

    def test_get_top_communities(self, test_client):
        """
        Test GET request to the /communities/top route to assert the page displays
        existing communities.
        """
        app_user = AppUser(username="mockusername", password="mockpassword")
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()

        response = test_client.get("/communities/top")

        assert response is not None
        assert response.status_code == 200
        assert bytes(community.name, "utf-8") in response.data
