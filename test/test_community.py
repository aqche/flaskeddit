from test import helpers

from passlib.hash import bcrypt

from flaskeddit import db
from flaskeddit.models import AppUser, Community


class TestCommunity:
    def test_get_community(self, test_client):
        """
        Test GET request to the /community/_ route to assert the community page is
        displayed.
        """
        app_user = AppUser(username="mockusername", password="mockpassword")
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()

        response = test_client.get(f"/community/{community.name}")

        assert response is not None
        assert response.status_code == 200
        assert bytes(community.name, "utf-8") in response.data

    def test_get_top_community(self, test_client):
        """
        Test GET request to the /community/_/top route to assert the community page is
        displayed.
        """
        app_user = AppUser(username="mockusername", password="mockpassword")
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()

        response = test_client.get(f"/community/{community.name}/top")

        assert response is not None
        assert response.status_code == 200
        assert bytes(community.name, "utf-8") in response.data

    def test_get_create_community(self, test_client):
        """
        Test GET request to the /community/create route to assert the community
        creation page is returned.
        """
        password = "Mockpassword123!"
        hashed_password = bcrypt.hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        db.session.add(app_user)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.get("/community/create")

        assert response is not None
        assert response.status_code == 200
        assert b"Create Community" in response.data

    def test_post_create_community(self, test_client):
        """
        Test POST request to the /community/create route to assert the community is
        successfully created.
        """
        password = "Mockpassword123!"
        hashed_password = bcrypt.hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        db.session.add(app_user)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.post(
            "/community/create",
            data={"name": "mockcommunity", "description": "mockdescription"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully created community" in response.data

    def test_get_update_community(self, test_client):
        """
        Test GET request to the /community/_/update route to assert the community
        update page is returned.
        """
        password = "Mockpassword123!"
        hashed_password = bcrypt.hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.get(f"/community/{community.name}/update")

        assert response is not None
        assert response.status_code == 200
        assert b"Update Community" in response.data

    def test_post_update_community(self, test_client):
        """
        Test POST request to the /community/_/update route to assert the community is
        successfully updated.
        """
        password = "Mockpassword123!"
        hashed_password = bcrypt.hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.post(
            f"/community/{community.name}/update",
            data={"description": "mockupdateddescription"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully updated community" in response.data

    def test_post_delete_community(self, test_client):
        """
        Test POST request to the /community/_/delete route to assert the community is
        successfully deleted.
        """
        password = "Mockpassword123!"
        hashed_password = bcrypt.hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.post(
            f"/community/{community.name}/delete", follow_redirects=True
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully deleted community" in response.data

    def test_post_join_community(self, test_client):
        """
        Test POST request to the /community/_/join route to assert the user
        successfully joined the community.
        """
        password = "Mockpassword123!"
        hashed_password = bcrypt.hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.post(
            f"/community/{community.name}/join", follow_redirects=True
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully joined community" in response.data

    def test_post_leave_community(self, test_client):
        """
        Test POST request to the /community/_/leave route to assert the user
        successfully left the community.
        """
        password = "Mockpassword123!"
        hashed_password = bcrypt.hash(password)
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()
        helpers.login(test_client, app_user.username, password)

        response = test_client.post(
            f"/community/{community.name}/leave", follow_redirects=True
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully left community" in response.data
