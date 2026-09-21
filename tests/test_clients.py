from unittest.mock import Mock

import orjson
import pytest

from bag_amsterdam_api.bevragingen.clients.base import BaseBagClient
from bag_amsterdam_api.bevragingen.clients.kadaster import BagClient
from bag_amsterdam_api.bevragingen.exceptions import (
    BadGateway,
    RemoteAPIException,
)


def make_response(status_code, body, content_type="application/json"):
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


def test_missing_endpoint_url():
    with pytest.raises(ValueError, match="Missing BAG endpoint URL"):
        BagClient("", api_key="key")


@pytest.mark.parametrize(
    ("status_code", "body", "expected"),
    [
        (400, {"title": "Validation"}, RemoteAPIException),
        (403, {"title": "Forbidden"}, RemoteAPIException),
        (500, {"title": "Server error"}, BadGateway),
    ],
)
def test_http_error_translation(status_code, body, expected):
    client = BagClient("https://example.com", api_key="key")

    response = make_response(status_code, body)

    error = client._get_http_error(response)

    assert isinstance(error, expected)


def test_api_key_added_to_session_headers():
    client = BaseBagClient(
        endpoint_url="https://example.com/api",
        api_key="secret",
    )

    assert client._session.headers["X-Api-Key"] == "secret"
