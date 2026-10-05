import logging
import time
from copy import deepcopy
from urllib.parse import urlsplit

import orjson
import requests
from django.conf import settings
from django.http import HttpResponse
from django.utils.timezone import now
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValError
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.views import APIView

from bag_amsterdam_api.bevragingen import authentication, exceptions, permissions
from bag_amsterdam_api.bevragingen.clients import BagClient
from bag_amsterdam_api.settings import URL

logger = logging.getLogger(__name__)


class BaseProxyView(APIView):
    """View that proxies kadaster BAG API.

    This is a pass-through proxy, but with authorization and extra restrictions added.
    The subclasses implement the variations between kadaster BAG endpoints.
    """

    authentication_classes = [authentication.JWTAuthentication]

    # Need to define for every subclass:

    #: An random short-name for the service name in logging statements
    service_log_id: str = None
    #: Which endpoint to proxy
    endpoint_url: str = None
    #: The base scopes needed for all requests
    needed_scopes: set = {"FP/MDW"}
    #: The query parameters needed for filtering
    query_parameters: type[BaseModel] | None = None

    def initial(self, request: Request, *args, **kwargs):
        """DRF-level initialization for all request types."""
        self.client = BagClient(
            endpoint_url=URL,
            api_key=settings.KADASTER_BAG_API_KEY,
        )
        self.start_time = time.perf_counter_ns()
        self.start_date = now()

        # Perform authorization, permission checks and throttles.
        super().initial(request, *args, **kwargs)

    def get_permissions(self):
        """Collect the DRF permission checks.
        DRF checks these in the initial() method, and will block view access
        if these permissions are not satisfied.
        """
        return super().get_permissions() + [
            permissions.IsUserScope(self.needed_scopes),
        ]

    def get(self, request: Request, *args, **kwargs):
        self.client.endpoint_url = self.get_endpoint_url()
        params = self.get_query_parameters(request)

        # Proxy to kadaster BAG API
        try:
            downstream_response = self.client.call(request, params)
        except (APIException, OSError) as e:
            response = (
                e.__cause__.response.json()
                if isinstance(e.__cause__, requests.RequestException)
                and e.__cause__.response is not None
                else None
            )
            raise

        # Rewrite the response to pagination still works.
        # (currently in in-place)
        response = orjson.loads(downstream_response.text)
        final_response = deepcopy(response)
        self.transform_response(request, final_response)
        # And return it.
        return HttpResponse(
            orjson.dumps(final_response),
            content_type=downstream_response.headers.get(
                "content-type", "application/hal+json; charset=utf-8"
            ),
        )

    def get_endpoint_url(self):
        """Format endpoint for detail views."""
        try:
            return self.endpoint_url.format(**self.kwargs)
        except KeyError:
            return self.endpoint_url

    def get_query_parameters(self, request):
        """Validate query parameters per endpoint with pydantic."""

        if not self.query_parameters:
            return None

        try:
            query_parameters = self.query_parameters.model_validate(request.query_params)
        except PydanticValError as e:
            raise exceptions.ParamsValidationError(self._convert_pydantic_error(e.errors())) from e

        params = query_parameters.model_dump(exclude_none=True)
        point = getattr(query_parameters, "point", None)
        if point is not None:
            params["point"] = query_parameters.point.to_query_param()

        return params

    def transform_response(self, request: dict, response: dict | list) -> None:
        """Replace hrefs in _links sections by whatever fn returns for them.

        May modify data in-place.
        """

        self._rewrite_links(
            response,
            rewrites=self.get_rewrites(request),
        )

    def get_rewrites(self, request):
        parts = urlsplit(self.client.endpoint_url)

        upstream_root = f"{parts.scheme}://{parts.netloc}/lvbag/individuelebevragingen/v2"

        return [
            (
                upstream_root,
                f"{request.build_absolute_uri('/')[:-1]}/individuelebevragingen/v2",
            )
        ]

    def _rewrite_links(self, data: dict | list, rewrites: list[tuple[str, str]]):
        if isinstance(data, list):
            # Lists: go level deeper
            for item in data:
                self._rewrite_links(item, rewrites)

        elif isinstance(data, dict):
            # First or second level: dict
            if isinstance(data.get("href"), str):
                href = data["href"]

                for find, replace in rewrites:
                    if href.startswith(find):
                        data["href"] = replace + href[len(find) :]

            for value in data.values():
                self._rewrite_links(value, rewrites)

    def _convert_pydantic_error(self, pydantic_errors: list) -> dict:
        invalid_params = []

        for error in pydantic_errors:
            invalid_params.append(
                {
                    "type": error.get("url"),
                    "name": ".".join(str(part) for part in error.get("loc", ())),
                    "code": error.get("type"),
                    "reason": error.get("msg"),
                }
            )

        return {
            "status": 400,
            "type": "https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#/10.4.1 "
            "400 Bad Request",
            "detail": pydantic_errors[0]["msg"],
            "instance": self.endpoint_url,
            "code": "paramsValidation",
            "invalid-params": invalid_params,
        }
