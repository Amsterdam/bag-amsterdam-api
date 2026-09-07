from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView

BASE_URL = settings.BAG_WP_URL


class WoonplaatsView(BaseProxyView):
    endpoint_url = BASE_URL
    service_log_id = "woonplaatsen"
    query_parameters = qp.WoonplaatsenQP


class WoonplaatsDetailView(BaseProxyView):
    base_url = settings.BAG_WP_URL
    endpoint_url = "{BASE_URL}/{id}"
    service_log_id = "woonplaatsen"
    query_parameters = qp.WoonplaatsenDetailQP


class WoonplaatsLvcView(BaseProxyView):
    base_url = settings.BAG_WP_URL
    endpoint_url = "{BASE_URL}/{id}/lvc"
    service_log_id = "woonplaatsen"
    query_parameters = qp.WoonplaatsenLvcQP


class WoonplaatsTimeRegistrationView(BaseProxyView):
    base_url = settings.BAG_WP_URL
    endpoint_url = "{BASE_URL}/{id}/{version}/{timestamp}"
    service_log_id = "woonplaatsen"
