from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class LigplaatsView(BaseProxyView):
    endpoint_url = settings.BAG_LP_URL
    service_log_id = "ligplaatsen"
    query_parameters = qp.LigplaatsenQP


class LigplaatsDetailView(BaseProxyView):
    endpoint_url = f"{settings.BAG_LP_URL}/{{id}}"
    service_log_id = "ligplaatsen-detail"
    query_parameters = qp.LigplaatsenDetailQP


class LigplaatsLvcView(BaseProxyView):
    endpoint_url = f"{settings.BAG_LP_URL}/{{id}}/lvc"
    service_log_id = "ligplaatsen-lvc"
    query_parameters = qp.LigplaatsenLvcQP


class LigplaatsTimeRegistrationView(BaseProxyView):
    endpoint_url = f"{settings.BAG_LP_URL}/{{id}}/{{version}}/{{timestamp}}"
    service_log_id = "ligplaatsen-tmr"
