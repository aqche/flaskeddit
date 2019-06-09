from flaskeddit import bcrypt, db
from flaskeddit.models import AppUser, Community


class TestCommunity:
    def test_get_community(self, test_client):
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
        assert b"mockcommunity" in response.data

    def test_get_top_community(self, test_client):
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
        assert b"mockcommunity" in response.data

    def test_get_create_community(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        app_user = AppUser(username="mockusername", password=hashed_password)
        db.session.add(app_user)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.get("/community/create")

        assert response is not None
        assert response.status_code == 200
        assert b"Create Community" in response.data

    def test_post_create_community(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        app_user = AppUser(username="mockusername", password=hashed_password)
        db.session.add(app_user)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.post(
            "/community/create",
            data={"name": "mockcommunity", "description": "mockdescription"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully created community" in response.data

    def test_get_update_community(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.get(f"/community/{community.name}/update")

        assert response is not None
        assert response.status_code == 200
        assert b"Update Community" in response.data

    def test_post_update_community(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.post(
            f"/community/{community.name}/update",
            data={"description": "mockupdateddescription"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully updated community" in response.data

    def test_post_delete_community(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.post(
            f"/community/{community.name}/delete", follow_redirects=True
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully deleted community" in response.data

    def test_post_join_community(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.post(
            f"/community/{community.name}/join", follow_redirects=True
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully joined community" in response.data

    def test_post_leave_community(self, test_client):
        hashed_password = bcrypt.generate_password_hash("Mockpassword123!")
        app_user = AppUser(username="mockusername", password=hashed_password)
        community = Community(
            name="mockcommunity", description="mockdescription", app_user=app_user
        )
        db.session.add(app_user)
        db.session.add(community)
        db.session.commit()
        test_client.post(
            "/login",
            data={"username": "mockusername", "password": "Mockpassword123!"},
            follow_redirects=True,
        )

        response = test_client.post(
            f"/community/{community.name}/leave", follow_redirects=True
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Successfully left community" in response.data
