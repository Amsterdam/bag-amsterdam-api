from unittest.mock import Mock

from bag_amsterdam_api.bevragingen.clients.kadaster import BagClient
from bag_amsterdam_api.bevragingen.exceptions import (
    BadGateway,
)


def test_get_non_json_response():
    """Prove that client handles non json responses"""
    client = BagClient("https://example.com", api_key="key")

    response = Mock()
    response.status_code = 500
    response.headers = {"content-type": "text/plain"}
    response.text = "Internal Server Error"

    error = client._get_http_error(response)

    assert isinstance(error, BadGateway)
