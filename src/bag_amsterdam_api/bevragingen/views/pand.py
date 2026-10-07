from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class PandView(BaseProxyView):
    endpoint_url = settings.BAG_PA_URL
    service_log_id = "panden"
    query_parameters = qp.PandenQP


class PandDetailView(BaseProxyView):
    endpoint_url = f"{settings.BAG_PA_URL}/{{id}}"
    service_log_id = "panden-detail"
    query_parameters = qp.PandenDetailQP


class PandLvcView(BaseProxyView):
    endpoint_url = f"{settings.BAG_PA_URL}/{{id}}/lvc"
    service_log_id = "panden-lvc"
    query_parameters = qp.PandenLvcQP


class PandTimeRegistrationView(BaseProxyView):
    endpoint_url = f"{settings.BAG_PA_URL}/{{id}}/{{version}}/{{timestamp}}"
    service_log_id = "panden-tmr"
