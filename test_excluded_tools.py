import pytest


# The pizza never needs a tool that the customer excluded.
# Blocks of "how many of the three tools are excluded": 0, 1, 2, 3.
# The block "3" is in its own test below, because it hits the defect.
@pytest.mark.parametrize(
    "excluded",
    [
        [],                      # block 0 tools
        ["Knife"],               # block 1 tool
        ["Scissors"],            # block 1 tool
        ["Knife", "Scissors"],   # block 2 tools
    ],
)
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# A request that no pizza can satisfy gets 400 and a JSON error, never 500.
@pytest.mark.xfail(
    reason="Defect 1: excluding all three tools gives 500 with an empty body",
    strict=True,
)
def test_all_tools_excluded_is_a_clean_error(api, auth):
    body = {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()
