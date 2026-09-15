import logging
import time
from copy import deepcopy

import orjson
import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.urls import reverse
from django.utils.timezone import now
from pydantic import ValidationError as PydanticValError
from rest_framework.exceptions import APIException, PermissionDenied, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from bag_amsterdam_api.bevragingen import authentication, permissions
from bag_amsterdam_api.bevragingen.clients.kadaster import BagClient
from bag_amsterdam_api.bevragingen.exceptions import RemoteAPIException
from bag_amsterdam_api.settings import URL

logger = logging.getLogger(__name__)


class ClientMixin(APIView):
    #: Define which additional scopes are needed
    client_class = BagClient

    #: Define the URL for the endpoint
    endpoint_url: URL

    def get_client(self) -> BagClient:
        """Provide the API client class. This can be overwritten per view if needed."""
        return self.client_class(
            endpoint_url=self.endpoint_url,
            api_key=settings.BAG_API_KEY,
        )


class BaseHealthCheckView(ClientMixin, APIView):
    """View that performs a dummy call to the BAG API for healthchecks."""

    authentication_classes = [authentication.JWTAuthentication]

    dummy_request = {"type": "healthcheck"}

    def get(self, request, *args, **kwargs):
        client = self.get_client()
        try:
            hc_response = client.call(self.dummy_request)
        except RemoteAPIException as e:
            success = e.detail == "De foutieve parameter(s) zijn: type."
            return Response({"success": success, "response": e.remote_json})
        except (APIException, OSError) as e:
            logger.error(
                "Proxy call to %s failed, error when connecting to server: %s",
                client.host,
                e,
            )
            return Response({"success": False, "exception": f"Proxy call to {client.host} failed"})

        return Response({"success": True, "response": hc_response})


class BaseProxyView(ClientMixin, APIView):
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
    #: The based scopes needed for all requests
    needed_scopes: set = {"fp_mdw"}
    #: The query parameters needed for filtering
    query_parameters: str = None

    def initial(self, request: Request, *args, **kwargs):
        """DRF-level initialization for all request types."""
        self._base_url = reverse(
            request.resolver_match.view_name,
            kwargs=request.resolver_match.kwargs,
        )
        self.client = self.get_client()
        self.start_time = time.perf_counter_ns()
        self.start_date = now()

        # Perform authorization, permission checks and throttles.
        super().initial(request, *args, **kwargs)

        # Options requests do not have a token in the header, so we'll return early
        if request.method == "OPTIONS":
            return

        # Token is validated, extract token scopes that are set by the middleware
        self.user_scopes = set(request.get_token_scopes)
        self.upn = request.get_token_claims.get("email", request.get_token_subject)
        self.appid = request.get_token_claims.get("appid")

        try:
            # request.data is only available in initial(), not in setup()
            self.default_log_fields = {
                "service": self.service_log_id,
                "queryType": request.data.get("type", None),
                "upn": self.upn,
                "user": self.request.headers["X-User"],
                "correlationId": self.request.headers["X-Correlation-ID"],
                "taskDescription": self.request.headers["X-Task-Description"],
                "granted": sorted(self.user_scopes),
            }
            if self.appid:
                self.default_log_fields["appid"] = self.appid
        except KeyError as e:
            raise PermissionDenied(
                f"A required header is missing: {e.args[0]}", code="missingHeaders"
            ) from None

    def get_permissions(self):
        """Collect the DRF permission checks.
        DRF checks these in the initial() method, and will block view access
        if these permissions are not satisfied.
        """
        if not self.needed_scopes:
            raise ImproperlyConfigured("needed_scopes is not set")

        return super().get_permissions() + [
            permissions.IsUserScope(self.needed_scopes),
        ]

    def get(self, request: Request, *args, **kwargs):
        self.client.endpoint_url = self.get_endpoint_url()
        hc_request = request.data.copy()
        params = self.get_query_parameters()

        # Proxy to kadaster BAG API
        try:
            downstream_response = self.client.call(hc_request, params)
        except (APIException, OSError) as e:
            # Even when the request failed, still log that we did grant access.
            hc_response = (
                e.__cause__.response.json()
                if isinstance(e.__cause__, requests.RequestException)
                and e.__cause__.response is not None
                else None
            )

        # Rewrite the response to pagination still works.
        # (currently in in-place)
        hc_response = orjson.loads(downstream_response.text)
        final_response = deepcopy(hc_response)
        # And return it.
        return HttpResponse(
            orjson.dumps(final_response),
            content_type=downstream_response.headers.get(
                "content-type", "application/json; charset=utf-8"
            ),
        )

    def get_endpoint_url(self):
        """Format endpoint for detail views."""
        try:
            return self.endpoint_url.format(**self.kwargs)
        except KeyError:
            return self.endpoint_url

    def get_query_parameters(self):
        """Validate query parameters per endpoint with pydantic."""

        try:
            query_parameters = self.query_parameters.model_validate(self.request.query_params)
        except PydanticValError as e:
            raise ValidationError({"detail": e.errors()}) from e

        params = query_parameters.model_dump(exclude_none=True)
        point = getattr(query_parameters, "point", None)
        if point is not None:
            params["point"] = query_parameters.point.to_query_param()

        return params
