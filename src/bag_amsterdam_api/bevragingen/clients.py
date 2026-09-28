import logging
import time
from urllib.parse import urlparse

import orjson
import requests
from requests import ConnectionError, Timeout
from rest_framework import status
from rest_framework.exceptions import APIException, NotFound

from bag_amsterdam_api.bevragingen.exceptions import (
    BadGateway,
    GatewayTimeout,
    RemoteAPIException,
    ServiceUnavailable,
)

logger = logging.getLogger(__name__)

USER_AGENT = "BAG-Amsterdam-API/1.0"


class BagClient:
    """
    BAG Client to consume BAG API's
    """

    # endpoint_url: URL

    def __init__(
        self,
        endpoint_url,
        *,
        api_key,
    ):
        """Initialize the client configuration.

        :param endpoint_url: Full URL of the BAG service.
        :param api_key: The API key to use
        """
        if not endpoint_url:
            raise ValueError("Missing BAG endpoint URL")
        self.endpoint_url = endpoint_url
        self._api_key = api_key
        self._host = urlparse(endpoint_url).netloc
        self._session = requests.Session()

        # persist api_key across session
        self._session.headers.update(
            {
                "X-Api-Key": api_key,
            }
        )

    @property
    def host(self) -> str:
        return self._host

    def call(
        self, request: dict | None = None, params: dict | None = None, *args, **kwargs
    ) -> requests.Response | APIException:
        """Make an HTTP GET call. kwargs are passed to pool.request."""
        logger.debug("calling %s", self.endpoint_url)
        t0 = time.perf_counter_ns()

        try:
            # Using urllib directly instead of requests for performance
            response: requests.Response = self._session.request(
                "GET",
                self.endpoint_url,
                json=request,
                params=params,
                timeout=60,
                headers={
                    "Accept": "application/hal+json; charset=utf-8",
                    "User-Agent": USER_AGENT,
                },
            )
        except (TimeoutError, Timeout) as e:
            # Socket timeout
            logger.error(
                "Proxy call to %s failed, timeout from remote server: %s",
                self._host,
                e,
            )
            raise GatewayTimeout() from e
        except (OSError, ConnectionError) as e:
            # Socket connect / SSL error.
            logger.error(
                "Proxy call to %s failed, error when connecting to server: %s",
                self._host,
                e,
            )
            raise ServiceUnavailable(str(e)) from e

        # Log response and timing results
        level = logging.ERROR if response.status_code >= 400 else logging.INFO
        logger.log(
            level,
            "Proxy call to %s, status %s: %s (%s), took: %.3fs",
            self.endpoint_url,
            response.status_code,
            response.reason,
            response.headers.get("content-type"),
            (time.perf_counter_ns() - t0) * 1e-9,
        )

        if 200 <= response.status_code < 300:
            return response

        # We got an error.
        # Raise exception in nicer format, but chain with the original one
        # so the "response" object is still accessible via __cause__.response.
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise self._get_http_error(response) from e

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
            if any(
                ct in content_type for ct in ["application/hal+json", "application/problem+json"]
            )
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
