from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class StandplaatsView(BaseProxyView):
    endpoint_url = settings.BAG_SP_URL
    service_log_id = "standplaatsen"
    query_parameters = qp.StandplaatsenQP


class StandplaatsDetailView(BaseProxyView):
    base_url = settings.BAG_SP_URL
    endpoint_url = "{base_url}/{id}"
    service_log_id = "standplaatsen"
    query_parameters = qp.StandplaatsenDetailQP


class StandplaatsLvcView(BaseProxyView):
    base_url = settings.BAG_SP_URL
    endpoint_url = "{base_url}/{id}/lvc"
    service_log_id = "standplaatsen"
    query_parameters = qp.StandplaatsenLvcQP


class StandplaatsTimeRegistrationView(BaseProxyView):
    base_url = settings.BAG_SP_URL
    endpoint_url = "{base_url}/{id}/{version}/{timestamp}"
    service_log_id = "standplaatsen"
