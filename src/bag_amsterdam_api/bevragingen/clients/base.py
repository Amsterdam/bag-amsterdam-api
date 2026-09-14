import logging
import time
from urllib.parse import urlparse

import requests
from requests import ConnectionError, Timeout
from rest_framework.exceptions import APIException

from bag_amsterdam_api.bevragingen.exceptions import GatewayTimeout, ServiceUnavailable

# from more_ds.network import URL
from bag_amsterdam_api.settings import URL

logger = logging.getLogger(__name__)

USER_AGENT = "BAG-Amsterdam-API/1.0"


class BaseBagClient:
    """
    Base BAG Client to consume BAG API's using a mtls connection
    """

    endpoint_url: URL

    def __init__(
        self,
        endpoint_url,
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

    def __repr__(self):
        return f"<{self.__class__.__qualname__}: {self.endpoint_url}>"

    def call(
        self, hc_request: dict | None = None, params: dict | None = None, *args, **kwargs
    ) -> requests.Response | APIException:
        """Make an HTTP GET call. kwargs are passed to pool.request."""
        logger.debug("calling %s", self.endpoint_url)
        t0 = time.perf_counter_ns()

        try:
            # Using urllib directly instead of requests for performance
            response: requests.Response = self._session.request(
                "GET",
                self.endpoint_url,
                json=hc_request,
                params=params,
                timeout=60,
                headers={
                    "Accept": "application/json; charset=utf-8",
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
        raise NotImplementedError
