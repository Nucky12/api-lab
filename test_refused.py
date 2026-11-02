import uuid


def new_user():
    name = "lab-" + uuid.uuid4().hex[:12]
    return {"username": name, "password": "Pizza-2026"}


# A second user with a name that is already taken gets 400.
def test_duplicate_username_is_refused(api):
    user = new_user()
    res = api.post("/api/users", json=user)
    assert res.status_code == 201
    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username already taken"}


# Logging in with a wrong password gets 401.
def test_wrong_password_is_refused(api):
    user = new_user()
    res = api.post("/api/users", json=user)
    assert res.status_code == 201
    wrong = {"username": user["username"], "password": "Wrong-Pass-1"}
    res = api.post("/api/users/token/login", json=wrong)
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


# A user with an empty name gets 400.
def test_empty_username_is_refused(api):
    res = api.post("/api/users", json={"username": "", "password": "Pizza-2026"})
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}
