"""Client for kadaster BAG API."""

import logging
from urllib.parse import urlparse

import orjson
import requests

# from more_ds.network.url import URL
from rest_framework import status
from rest_framework.exceptions import APIException, NotFound

from bag_amsterdam_api.bevragingen.exceptions import (
    BadGateway,
    RemoteAPIException,
)

from .base import BaseBagClient

logger = logging.getLogger(__name__)

USER_AGENT = "BAG-Amsterdam-API/1.0"


class BagClient(BaseBagClient):
    """kadaster BAG API client.

    When a reference to the client is kept globally,
    its HTTP connection pool can be reused between threads.
    """

    def __init__(
        self,
        endpoint_url,
        *,
        api_key,
    ):
        """Initialize the client configuration.

        :param endpoint_url: Full URL of the kadaster BAG service.
        :param api_key: The API key to use
        """
        if not endpoint_url:
            raise ValueError("Missing BAG endpoint URL")
        self.endpoint_url = endpoint_url
        self._api_key = api_key
        self._host = urlparse(endpoint_url).netloc
        self._session = requests.Session()

    @property
    def host(self) -> str:
        return self._host

    def _get_http_error(self, response: requests.Response) -> APIException:
        # Translate the remote HTTP error to the proper response.
        #
        # This translates some errors into a 502 "Bad Gateway" or 503 "Gateway Timeout"
        # error to reflect the fact that this API is calling another service as backend.

        # Consider the actual JSON response here,
        # unless the request hit the completely wrong page (it got an HTML page).
        content_type = response.headers.get("content-type", "")
        remote_json = (
            orjson.loads(response.content)
            if any(ct in content_type for ct in ["application/json", "application/problem+json"])
            else None
        )
        detail_message = response.text if not content_type.startswith("text/html") else None

        if not remote_json:
            # Unexpected response, call it a "Bad Gateway"
            logger.error(
                "Proxy call failed, unexpected status code from endpoint: %s %s",
                response.status_code,
                detail_message,
            )
            return BadGateway(
                detail_message or f"Unexpected HTTP {response.status_code} from internal endpoint"
            )

        if response.status_code == status.HTTP_401_UNAUTHORIZED or (
            response.status_code == status.HTTP_403_FORBIDDEN
            and remote_json is not None
            and remote_json["title"] == "U bent niet geautoriseerd voor het gebruik van deze API."
        ):
            # Our API key is not configured (401) or incorrect (403). Don't blame the client.
            # So far there is no other cause for a 403, but allow this to change.
            return BadGateway(
                "Backend is improperly configured, final endpoint rejected our credentials.",
                code="backend_config",
            )
        elif response.status_code in (
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN,
        ):
            # Bad request likely means the JSON parameters were invalid.
            # Translate proper "Bad Request" to REST response
            return RemoteAPIException(response.status_code, remote_json)
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            # Return 404 to client (in DRF format)
            if content_type == "application/problem+json":
                # Forward the problem-json details, but still in a 404:
                return RemoteAPIException(response.status_code, remote_json)
            return NotFound(repr(remote_json))
        else:
            # Unexpected response, call it a "Bad Gateway"
            logger.error(
                "Proxy call failed, unexpected status code from endpoint: %s %s",
                response.status_code,
                detail_message,
            )
            return BadGateway(f"Unexpected HTTP {response.status_code} from internal endpoint")
