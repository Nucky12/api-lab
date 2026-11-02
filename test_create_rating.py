import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"
AUTH_ERROR = {"error": "authentication failed"}


# Base choice: 3 stars as a whole number, a real pizza, the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id


# C1: a number of stars below 1 or above 5 is refused with a message.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2: stars as a decimal number is refused.
# TODO: check the exact status and message with curl, then tighten the asserts.
def test_stars_decimal(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3.5}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()


# C2: stars as text is refused.
# TODO: check the exact status and message with curl, then tighten the asserts.
def test_stars_text(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": "3"}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()


# C2: a body without the stars field is refused.
# TODO: check the exact status and message with curl, then tighten the asserts.
def test_stars_missing(api, auth, pizza_id):
    new = {"pizza_id": pizza_id}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()


# C3: a pizza that does not exist is refused.
# TODO: check the exact status and message with curl, then tighten the asserts.
def test_pizza_does_not_exist(api, auth):
    new = {"pizza_id": 999999999, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert 400 <= res.status_code <= 499
    assert "error" in res.json()


# C4: a request without the Authorization header is refused with 401.
def test_no_token(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new)
    assert res.status_code == 401
    assert res.json() == AUTH_ERROR


# C4: a token of the wrong length is refused with 401.
# TODO: check the exact message with curl.
def test_token_too_short(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new,
                   headers={"Authorization": "token short"})
    assert res.status_code == 401
    assert res.json() == AUTH_ERROR
