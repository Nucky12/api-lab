# Another user must not read the rating of its owner.
def test_other_user_cannot_read(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.get(path, headers=other_auth)
    print("READ status:", res.status_code)
    assert 400 <= res.status_code <= 499
    assert api.get(path, headers=auth).json() == rating


# Another user must not change the rating of its owner.
def test_other_user_cannot_change(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 1}, headers=other_auth)
    print("CHANGE status:", res.status_code)
    assert 400 <= res.status_code <= 499
    assert api.get(path, headers=auth).json() == rating


# Another user must not delete the rating of its owner.
def test_other_user_cannot_delete(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.delete(path, headers=other_auth)
    print("DELETE status:", res.status_code)
    assert 400 <= res.status_code <= 499
    assert api.get(path, headers=auth).json() == rating
