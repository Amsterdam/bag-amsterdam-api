import logging
import time

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.utils.timezone import now
from pydantic import ValidationError as PydanticValError
from rest_framework.exceptions import APIException, PermissionDenied, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from rest_framework.views import APIView

from bag_amsterdam_api.bevragingen import authentication, permissions
from bag_amsterdam_api.bevragingen.clients.rvig import RvIGBagClient
from bag_amsterdam_api.bevragingen.exceptions import RemoteAPIException
from bag_amsterdam_api.settings import URL

logger = logging.getLogger(__name__)

# DictOfDicts = dict[str, dict[str, dict]]


class ClientMixin(APIView):
    #: Define which additional scopes are needed
    client_class = RvIGBagClient

    #: Define the URL for the endpoint
    endpoint_url: URL

    def get_client(self) -> RvIGBagClient:
        """Provide the API client class. This can be overwritten per view if needed."""
        return self.client_class(
            endpoint_url=self.endpoint_url,
            oauth_endpoint_url=settings.BAG_OAUTH_TOKEN_URL,
            oauth_client_id=settings.BAG_OAUTH_CLIENT_ID,
            oauth_client_secret=settings.BAG_OAUTH_CLIENT_SECRET,
            oauth_scope=settings.BAG_OAUTH_SCOPE,
        )


class BaseHealthCheckView(ClientMixin, APIView):
    """View that performs a dummy call to the BAG API for healthchecks."""

    authentication_classes = [authentication.JWTAuthentication]
    throttle_classes = [AnonRateThrottle, ScopedRateThrottle]

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
    """View that proxies RvIG BAG API.

    This is a pass-through proxy, but with authorization and extra restrictions added.
    The subclasses implement the variations between RvIG BAG endpoints.
    """

    authentication_classes = [authentication.JWTAuthentication]

    # Need to define for every subclass:

    #: An random short-name for the service name in logging statements
    service_log_id: str = None
    #: Which endpoint to proxy
    endpoint_url: str = None
    #: The based scopes needed for all requests
    needed_scopes: set = {"fp_mdw"}
    #: The filter dto's needed for filtering
    filter_dto: str = None

    def initial(self, request: Request, *args, **kwargs):
        """DRF-level initialization for all request types."""
        self._base_url = reverse(request.resolver_match.view_name)
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

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryparams(self):
        # stuurt alleen data door, dus alleen check als er query_params
        # zijn, zijn deze dan voor dit endpoint geldig uit de lijst query_params voor
        # dit endpoint en zijn ze van het juiste type?
        # dus extract query params, transformeer naar dto, check of deze onder endpoint vallen,
        # check of ze juiste type hebben, en als gevalideerd stuur door, anders thro exception?
        try:
            filter_dto = self.filter_dto.model_validate(self.request.query_params)
        except PydanticValError as e:
            raise ValidationError(e.errors()) from e

        return filter_dto.model_dump(exclude_none=True)
