def login(test_client, username, password):
    """Logs in a user."""
    test_client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )
