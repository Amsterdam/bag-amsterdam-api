import json

from django.test import RequestFactory

from bag_amsterdam_api.views import (
    ProblemJsonException,
    bad_request,
    exception_handler,
    not_found,
    server_error,
)


def test_pulse(api_client):
    response = api_client.get("/pulse")
    assert response.status_code == 200
    assert response.data == {"status": "OK"}


def test_bad_request_handler():
    request = RequestFactory().get("/")

    response = bad_request(request, Exception())

    data = json.loads(response.content)

    assert response.status_code == 400
    assert data["title"] == "Bad Request (400)"


def test_not_found_handler():
    request = RequestFactory().get("/")

    response = not_found(request, Exception())

    data = json.loads(response.content)

    assert response.status_code == 404
    assert data["title"] == "Not Found (404)"


def test_server_error_handler():
    request = RequestFactory().get("/")

    try:
        raise RuntimeError("boom")
    except RuntimeError:
        response = server_error(request)

    data = json.loads(response.content)

    assert response.status_code == 500
    assert data["title"] == "Server Error (500)"


def test_problem_json_exception_with_invalid_params():
    request = RequestFactory().get("/test")

    exc = ProblemJsonException(
        title="Bad Request",
        detail="Invalid",
        code=400,
        invalid_params=[{"name": "postcode", "reason": "invalid"}],
    )

    response = exception_handler(exc, {"request": request})

    assert response.data["invalidParams"] == [{"name": "postcode", "reason": "invalid"}]
