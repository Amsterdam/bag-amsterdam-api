from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class StandplaatsView(BaseProxyView):
    endpoint_url = settings.BAG_SP_URL
    service_log_id = "standplaatsen"
    query_parameters = qp.StandplaatsenQP


class StandplaatsDetailView(BaseProxyView):
    endpoint_url = f"{settings.BAG_SP_URL}/{{id}}"
    service_log_id = "standplaatsen-detail"
    query_parameters = qp.StandplaatsenDetailQP


class StandplaatsLvcView(BaseProxyView):
    endpoint_url = f"{settings.BAG_SP_URL}/{{id}}/lvc"
    service_log_id = "standplaatsen-lvc"
    query_parameters = qp.StandplaatsenLvcQP


class StandplaatsTimeRegistrationView(BaseProxyView):
    endpoint_url = f"{settings.BAG_SP_URL}/{{id}}/{{version}}/{{timestamp}}"
    service_log_id = "standplaatsen-tmr"
