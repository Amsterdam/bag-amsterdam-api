from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class LigplaatsView(BaseProxyView):
    endpoint_url = settings.BAG_LP_URL
    service_log_id = "ligplaatsen"
    query_parameters = qp.LigplaatsenQP


class LigplaatsDetailView(BaseProxyView):
    base_url = settings.BAG_LP_URL
    endpoint_url = "{base_url}/{id}"
    service_log_id = "ligplaatsen"
    query_parameters = qp.LigplaatsenDetailQP


class LigplaatsLvcView(BaseProxyView):
    base_url = settings.BAG_LP_URL
    endpoint_url = "{base_url}/{id}/lvc"
    service_log_id = "ligplaatsen"
    query_parameters = qp.LigplaatsenLvcQP


class LigplaatsTimeRegistrationView(BaseProxyView):
    base_url = settings.BAG_LP_URL
    endpoint_url = "{base_url}/{id}/{version}/{timestamp}"
    service_log_id = "ligplaatsen"
