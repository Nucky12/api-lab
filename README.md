# api-lab

API tests for QuickPizza (https://quickpizza.grafana.com) with pytest and requests.

## Install and run

    python3 -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    pytest -v
    pytest -v --html=report.html --self-contained-html

A full run sends about 140 requests and takes about a minute. Expected result: 32 passed, 1 xfailed.
The xfailed test is a known defect (see RESULTS.md, Defect report).

## Files

- `conftest.py`: shared fixtures (one session, a new user for each test, a pizza, a rating).
- `test_create_rating.py`: input space partitioning for `POST /api/ratings`.
- `test_update_rating.py`: boundary values for `PUT /api/ratings/{id}`.
- `test_rating_owner.py`: another user must not read, change or delete a rating.
- `test_excluded_tools.py`: blocks of "how many tools are excluded", with the known defect as xfail.
- Other `test_*.py` files: the steps of Part 0.
- `RESULTS.md`: results, defect report and answers to the reflection questions.

## How the inputs were derived

The fields of a request are the inputs of an operation. For `POST /api/ratings` the rules of the API are: stars is a whole number from 1 to 5, the pizza must exist, and the request needs the token of a logged-in user. From these rules I took four characteristics and split each one into blocks that do not overlap and together cover every value. I then used base choice coverage: one base test uses the base block of every characteristic, and each other test changes one characteristic to one non-base block and keeps the rest at the base. For the boundaries of the stars rule, `PUT /api/ratings/{id}` is tested with 0, 1, 5 and 6.

## Input domain model for POST /api/ratings

| Characteristic | Block | Value | Covered by |
|---|---|---|---|
| C1 Value of stars | 1 to 5 (base) | 3 | test_base_choice_is_saved |
| C1 Value of stars | below 1 | 0 | test_stars_out_of_range[0] |
| C1 Value of stars | above 5 | 6 | test_stars_out_of_range[6] |
| C2 Type of stars | whole number (base) | 3 | test_base_choice_is_saved |
| C2 Type of stars | decimal | 3.5 | test_stars_decimal |
| C2 Type of stars | text | "3" | test_stars_text |
| C2 Type of stars | missing | no field | test_stars_missing |
| C3 Pizza | exists (base) | a new pizza | test_base_choice_is_saved |
| C3 Pizza | does not exist | 999999999 | test_pizza_does_not_exist |
| C4 Token | the user's own (base) | from auth | test_base_choice_is_saved |
| C4 Token | none | no header | test_no_token |
| C4 Token | wrong length | token short | test_token_too_short |

Base choice needs 1 + 2 + 3 + 1 + 2 = 9 tests. All combinations would need 3 x 4 x 2 x 3 = 72.