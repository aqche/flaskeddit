def login(test_client, username, password):
    """
    Helper to log in a user with the test client.
    """
    test_client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )
