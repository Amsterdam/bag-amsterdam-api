from unittest.mock import Mock

import orjson
import pytest
import requests
from requests.exceptions import Timeout
from rest_framework.exceptions import APIException, NotFound

from bag_amsterdam_api.bevragingen.clients import BagClient
from bag_amsterdam_api.bevragingen.exceptions import (
    BadGateway,
    GatewayTimeout,
    RemoteAPIException,
    ServiceUnavailable,
)


def make_response(status_code, body, content_type="application/hal+json"):
    response = Mock()
    response.status_code = status_code
    response.headers = {"content-type": content_type}
    response.content = orjson.dumps(body)
    response.text = str(body)
    return response


def test_get_non_json_response():
    """Prove that client handles non json responses"""
    client = BagClient("https://example.com", api_key="key")

    response = Mock()
    response.status_code = 500
    response.headers = {"content-type": "text/plain"}
    response.text = "Internal Server Error"

    error = client._get_http_error(response)

    assert isinstance(error, BadGateway)


def test_http_error(requests_mock):
    """Prove that client handles non json responses"""
    client = BagClient("https://example.com/adressen", api_key="key")
    requests_mock.get(
        "https://example.com/adressen", status_code=500, json={"error": "Internal Server Error"}
    )
    request = Mock()
    request.data = {}

    with pytest.raises(APIException) as exc_info:
        client.call(request)

    assert isinstance(exc_info.value.__cause__, requests.HTTPError)


def test_missing_endpoint_url():
    with pytest.raises(ValueError, match="Missing BAG endpoint URL"):
        BagClient("", api_key="key")


@pytest.mark.parametrize(
    ("status_code", "body", "expected"),
    [
        (400, {"title": "Validation"}, RemoteAPIException),
        (403, {"title": "Forbidden"}, RemoteAPIException),
        (404, {"title": "Not found"}, NotFound),
        (500, {"title": "Server error"}, BadGateway),
    ],
)
def test_http_error_translation(status_code, body, expected):
    client = BagClient("https://example.com", api_key="key")
    response = make_response(status_code, body)
    error = client._get_http_error(response)

    assert isinstance(error, expected)


def test_api_key_added_to_session_headers():
    client = BagClient(
        endpoint_url="https://example.com/api",
        api_key="secret",
    )

    assert client._session.headers["X-Api-Key"] == "secret"


def test_timeout(requests_mock):
    client = BagClient(endpoint_url="https://example.com/adressen", api_key="key")
    requests_mock.get(
        "https://example.com/adressen",
        exc=Timeout,
    )

    request = Mock()
    request.data = {}

    with pytest.raises(GatewayTimeout) as exc_info:
        client.call(request)

    assert isinstance(exc_info.value.__cause__, Timeout)


def test_connection(requests_mock):
    client = BagClient(endpoint_url="https://example.com/adressen", api_key="key")
    requests_mock.get(
        "https://example.com/adressen",
        exc=ConnectionError,
    )

    request = Mock()
    request.data = {}

    with pytest.raises(ServiceUnavailable) as exc_info:
        client.call(request)

    assert isinstance(exc_info.value.__cause__, ConnectionError)
