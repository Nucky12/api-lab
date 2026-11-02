import pytest


# Boundary values for stars on update: 1 and 5 are saved, 0 and 6 are refused,
# and a refused update leaves the rating as it was.
@pytest.mark.parametrize("stars, expected", [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_boundaries(api, auth, rating, stars, expected):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected

    saved = stars if expected == 200 else rating["stars"]
    res = api.get(path, headers=auth)
    assert res.status_code == 200
    assert res.json()["stars"] == saved
