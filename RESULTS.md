# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: The Light Marinara
- Step 0.12, results of the three runs without a session (optional): not done (optional step)
- Step 0.16, blocks of "how many of the three tools are excluded":
  - 0 tools excluded (added to the test, passes)
  - 1 tool excluded (the two original inputs, `["Knife"]` and `["Scissors"]`)
  - 2 tools excluded (added to the test, passes)
  - 3 tools excluded, all of them (moved to its own test, reveals the defect)

## Defect report
- Title: Excluding all three tools makes /api/pizza answer 500 with an empty body
- Request: `POST https://quickpizza.grafana.com/api/pizza` with header `Authorization: token <valid token>` and body `{"excludedTools": ["Knife","Pizza cutter","Scissors"]}`
- Expected result: status 400 and a JSON error message, because no pizza can satisfy the request
- Actual result: status `500 Internal Server Error` with `Content-Length: 0`, so there is no body and no error message (confirmed with `curl.exe -i` on 2 November 2026)
- Severity: Medium. The request is valid-looking and a customer can send it by mistake. The server fails and the calling app gets no message to show. No data is lost or exposed.

## Part A
- Step A4, status codes when the other user reads, changes and deletes:
  - read: 404
  - change: 400
  - delete: 400

## Part B
1. Two kinds of failure that tests against the real server can find and a unit test with stubs cannot: (a) infrastructure problems between the parts, for example the load balancer sending a login to a server that does not know the new user, and (b) a server that crashes on a real input, for example the 500 with an empty body when all three tools are excluded. A stub only returns what we told it to return, so it cannot show how the real system behaves. We should still write unit tests with stubs, because they run fast, do not need the network, give the same result every time, and point to the exact function that is broken.

2. The public token is shared by everyone who practises on QuickPizza, so another student could change or delete the same ratings while my test runs, and the result would depend on other people. A new user with a new random name owns its own data, so no other test or person can disturb it. In Project 2 I will apply the same idea to the shared shop or hotel: each test creates the products, customers, carts or bookings that it needs, with unique names, uses only those, and deletes them afterwards, so my tests never touch the data of other groups.

3. A `requests.Session` keeps the cookies that the site sends, including `AWSALB`. This cookie tells the load balancer which server to use, so every request of the run reaches the same server, the one that holds the user we just created. Without a session each request may reach a different server, and the login can fail with 401 for a user that exists on another server. That makes the test flaky. (I did not do the optional Step 0.12, so I have no results of my own for the three runs.)

4. The block that revealed the defect is the one where all three tools are excluded. The curl request returned `500 Internal Server Error` with `Content-Length: 0`. A 500 with an empty body is worse for an app than a 400 with a message, because the app cannot tell whether its own request was wrong or the server broke, it cannot tell the user what to change, and it has nothing to log. A 400 with a message says what was wrong and that the client can fix it. The test stays in the suite as xfail instead of being deleted, because the defect stays visible in every run, the rest of the suite stays green, and with `strict=True` the run fails as soon as QuickPizza fixes the defect, which tells us to remove the mark.

5. The model in Step A1 has four characteristics with 3, 4, 2 and 3 blocks. Base choice coverage needs one base test, plus one test for each non-base block: (3-1) + (4-1) + (2-1) + (3-1) = 2 + 3 + 1 + 2 = 8, so 1 + 8 = **9 tests**. All combinations coverage needs 3 x 4 x 2 x 3 = **72 tests**.

6. When the other user tried to read the rating of the owner, the status was 404. For change and for delete it was 400. In all three cases the attempt was refused and the owner's rating stayed the same, so the important requirement holds. I would expect 403 Forbidden (the user is known but not allowed) for change and delete, and 403 or 404 for read (404 is acceptable if the API wants to hide that the rating exists). The 400 for change and delete is not a security defect, but it is a small defect in the API design: 400 means that the request itself is malformed, which is not true here, and the three operations answer inconsistently (404 for read, 400 for the others). I would report it with low severity.

7. The request with the made-up token `0000000000000000` returned `200 OK` and a JSON list of about 50 ratings, instead of 401. I think this is a defect, because the server accepted a token that it never issued, so the authentication on this operation does not work as it should. (The exact reason is not clear from outside. The server may treat any unknown token as a default shared user.) On a real system a stranger could read data that belongs to other users without an account. If other operations behave the same way, which I did not test and must not test, a stranger could also create, change or delete data. I only read with this token and did not create or change anything.

8. An API test checks the exact status codes, error messages and JSON fields better than a test through the web pages, and it can send inputs that the web page would never allow, for example 0 stars, text instead of a number, or no token. It is also faster and more stable. Only a test through the web pages can check what the user really sees and does in the browser, for example that the page is laid out correctly, that the button is visible and clickable, and that the JavaScript on the page shows the right message.